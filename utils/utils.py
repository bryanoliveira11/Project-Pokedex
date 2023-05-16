def format_id(poke_id):
    if poke_id < 10:
        return f"#00{poke_id}"
    elif poke_id >= 10 and poke_id < 100:
        return f"#0{poke_id}"
    else:
        return f"#{poke_id}"
