def is_shariah_compliant(info):
    sector = str(info.get("sector", "")).lower()
    industry = str(info.get("industry", "")).lower()

    # Haram sectors
    haram_keywords = [
        "bank",
        "financial",
        "insurance",
        "alcohol",
        "gambling",
        "tobacco",
        "casino",
        "interest",
        "lending"
    ]

    for keyword in haram_keywords:
        if keyword in sector or keyword in industry:
            return False

    # Debt ratio filter
    debt_to_equity = info.get("debtToEquity", 0)

    if debt_to_equity and debt_to_equity > 33:
        return False

    return True