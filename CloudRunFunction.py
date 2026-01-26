import os
import sqlalchemy
import pg8000
from google.cloud.sql.connector import Connector, IPTypes
import functions_framework

# Initialize connector globally
connector = Connector(refresh_strategy="LAZY")


def _require_env(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(f"Missing required env var: {name}")
    return val


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "t", "yes", "y", "on"}


def getconn() -> pg8000.dbapi.Connection:
    private_ip = os.getenv("PRIVATE_IP", "").lower() in {"1","true","yes","on"}
    ip_type = IPTypes.PRIVATE if private_ip else IPTypes.PUBLIC

    db_user = os.environ["DB_USER"]  # must be ...@developer.iam
    print("********************************")
    print(f"PRIVATE_IP={os.getenv('PRIVATE_IP')} ip_type={ip_type.name} DB_USER={db_user}")

    return connector.connect(
        os.environ["INSTANCE_CONNECTION_NAME"],
        "pg8000",
        user=db_user,
        db=os.environ["DB_NAME"],
        enable_iam_auth=True,
        ip_type=ip_type,
        timeout=10,
    )

engine = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
    pool_timeout=10,
    pool_pre_ping=True,
)



engine = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
    # SQLAlchemy-side fast-fail protections:
    pool_timeout=10,     # wait max 10s for a pooled connection
    pool_pre_ping=True,  # detect stale connections quickly
)


@functions_framework.http
def hello_http(request):
    try:
        print("**************VOLARE***********************")
        with engine.connect() as conn:
            res = conn.execute(sqlalchemy.text("SELECT current_user")).fetchone()
            return f"Success! Authenticated as: {res[0]}"
    except Exception as e:
        return f"Auth Error: {e}", 500
