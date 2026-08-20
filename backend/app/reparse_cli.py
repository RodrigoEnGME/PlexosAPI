import argparse
import json
from pathlib import Path

from app.db import SessionLocal, init_db
from app.services.reparse import reparse_all_revisions


def main() -> None:
    parser = argparse.ArgumentParser(description="Reparse dated SDDP modifications for stored revisions")
    parser.add_argument("--artifact-root", default="data/artifacts")
    parser.add_argument("--data-root", default="data")
    args = parser.parse_args()
    data_root = Path(args.data_root)
    fallback_roots = {
        "CRIE Gatun": data_root / "PA_202503_R25_1050_Gatun_en_BC02",
        "Uruguay": data_root / "UY_SDDP",
        "PE_BC": data_root / "PE_BC",
        "Rep Dominicana": data_root / "RD_Tomas" / "BC01",
    }
    init_db()
    db = SessionLocal()
    try:
        results = reparse_all_revisions(db, args.artifact_root, fallback_roots)
        print(json.dumps([result.__dict__ for result in results], ensure_ascii=False, indent=2))
    finally:
        db.close()


if __name__ == "__main__":
    main()
