from dataclasses import asdict
from .models import FetchResult
import json
from pathlib import Path

def save_results(results : list[FetchResult],output_path : str) -> None:
    result_dict=[asdict(result) for result in results]
    path=Path(output_path)
    path.parent.mkdir(parents=True,exist_ok=True)

    with path.open("w",encoding="utf-8") as file:
        json.dump(result_dict,file,indent=4)




