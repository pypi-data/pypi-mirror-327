from huggingface_hub import HfApi
from rich import print
from rich.progress import Progress

def fingerprint(name, token):
    print("[bold yellow]🔍 Retrieving dataset fingerprint from HuggingFace Hub...[/bold yellow]")
    api = HfApi(token=token)
    info = api.model_info(name)
    print(f"[bold yellow]✔ Fingerprint (SHA) retrieved: {info.sha}[/bold yellow]")
    return info.sha


FILE_TYPES = [
    ".py",
    ".md",
    "LICENSE",
    ".json",
    ".yaml",
    ".yml",
    ".txt",
    ".safetensors",
    ".model",
    ".bin",
]


def load(name, token, directory):
    api = HfApi(token=token)
    info = api.repo_info(name, repo_type="model")
    siblings = info.siblings

    # Filter siblings by file type
    siblings = [
        sibling
        for sibling in siblings
        if any(file_type in sibling.rfilename for file_type in FILE_TYPES)
    ]

    # Download files sequentially with a Rich progress bar
    with Progress() as progress:
        task = progress.add_task("[green]Downloading files...", total=len(siblings))
        for sibling in siblings:
            api.hf_hub_download(
                repo_id=name,
                filename=sibling.rfilename,
                repo_type="model",
                token=token,
                local_dir=directory,
            )
            progress.advance(task)
    return info.sha
