def log(s: str, lvl=1):
    assert lvl > 0
    print(
        f"{' '*4*(lvl-1)}-> {s}"
    )
