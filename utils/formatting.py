def format_number(num):
    """Formats a number with K/M/B suffixes and thousand separators."""
    if num is None or num == 'N/A':
        return 'N/A'
    try:
        num = float(num)
        if num >= 1_000_000_000:
            return f"{num/1_000_000_000:,.2f}B"
        if num >= 1_000_000:
            return f"{num/1_000_000:,.2f}M"
        if num >= 1_000:
            return f"{num/1_000:,.2f}K"
        return f"{num:,.2f}"
    except:
        return num
