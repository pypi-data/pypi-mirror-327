from py_secscan import process
from py_secscan import stdx
import os


def main():
    try:
        process.run_subprocess(
            f"streamlit run {os.path.join(os.path.dirname(__file__), 'webapp.py')}",
        )
    except KeyboardInterrupt:
        stdx.error("Manual interruption")
