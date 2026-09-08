MONOGRAM = {
    "E": 12.02, "T": 9.10, "A": 8.12, "O": 7.68, "I": 7.31, "N": 6.95,
    "S": 6.28, "R": 6.02, "H": 5.92, "D": 4.32, "L": 3.98, "U": 2.88,
    "C": 2.71, "M": 2.61, "F": 2.30, "Y": 2.11, "W": 2.09, "G": 2.03,
    "P": 1.82, "B": 1.49, "V": 1.11, "K": 0.69, "X": 0.17, "Q": 0.11,
    "J": 0.10, "Z": 0.07,
}

BIGRAM = {
    "TH": 3.56, "HE": 3.07, "IN": 2.43, "ER": 2.05, "AN": 1.99, "RE": 1.85,
    "ON": 1.76, "AT": 1.49, "EN": 1.45, "ND": 1.35, "TI": 1.34, "ES": 1.34,
    "OR": 1.28, "TE": 1.24, "OF": 1.17, "ED": 1.17, "IS": 1.13, "IT": 1.12,
    "AL": 1.09, "AR": 1.07, "ST": 1.05, "TO": 1.05, "NT": 1.04, "NG": 0.95,
    "SE": 0.93, "HA": 0.93, "AS": 0.87, "OU": 0.87, "IO": 0.83, "LE": 0.83,
    "VE": 0.83, "CO": 0.79, "ME": 0.79, "DE": 0.76, "HI": 0.76, "RI": 0.73,
    "RO": 0.73, "IC": 0.70, "NE": 0.69, "EA": 0.69, "RA": 0.69, "CE": 0.65,
    "LI": 0.62, "CH": 0.60, "LL": 0.58, "BE": 0.58, "MA": 0.57, "SI": 0.55,
    "OM": 0.55, "UR": 0.54, "CA": 0.54, "OW": 0.53, "SS": 0.52, "PE": 0.51,
    "IL": 0.51, "AD": 0.50, "EL": 0.49, "OL": 0.49, "SO": 0.49, "AC": 0.48,
    "PR": 0.47, "US": 0.46, "GH": 0.45, "PA": 0.45, "UN": 0.44, "EC": 0.44,
    "TA": 0.44, "AM": 0.43, "LO": 0.43, "TR": 0.43, "AI": 0.42, "EM": 0.41,
    "WA": 0.40, "MI": 0.40, "WI": 0.40, "OT": 0.39, "TU": 0.39,
}

TRIGRAM = {
    "THE": 1.81, "AND": 0.73, "ING": 0.72, "ENT": 0.42, "ION": 0.42,
    "HER": 0.36, "FOR": 0.34, "THA": 0.33, "NTH": 0.33, "INT": 0.32,
    "ERE": 0.31, "TIO": 0.31, "TER": 0.30, "EST": 0.28, "ERS": 0.28,
    "ATI": 0.26, "HAT": 0.26, "ATE": 0.25, "ALL": 0.25, "VER": 0.24,
    "HIS": 0.24, "ONT": 0.24, "ETH": 0.24, "RES": 0.21, "MEN": 0.21,
    "EAR": 0.20, "WIT": 0.20, "HES": 0.20, "OME": 0.20, "HAS": 0.19,
    "WAS": 0.19, "HED": 0.19, "IST": 0.19, "INE": 0.18, "THI": 0.18,
    "ANT": 0.18, "ITH": 0.18, "OUR": 0.18, "OTH": 0.17, "ART": 0.17,
    "STH": 0.17, "ELL": 0.16, "ATT": 0.16, "OFT": 0.16, "ERA": 0.16,
    "ITS": 0.16, "TTH": 0.16, "ROM": 0.15, "AIN": 0.15, "PRO": 0.15,
}

DOUBLES = ["LL", "EE", "SS", "OO", "TT", "FF", "RR", "NN", "PP", "CC", "MM", "DD", "GG"]

COMMON_WORDS = {
    1: ["A", "I"],
    2: ["OF", "TO", "IN", "IT", "IS", "BE", "AS", "AT", "SO", "WE", "HE",
        "BY", "OR", "ON", "DO", "IF", "ME", "MY", "UP", "AN", "GO", "NO",
        "US", "AM"],
    3: ["THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL", "ANY", "CAN",
        "HAD", "HER", "WAS", "ONE", "OUR", "OUT", "DAY", "GET", "HAS", "HIM",
        "HIS", "HOW", "MAN", "NEW", "NOW", "OLD", "SEE", "TWO", "WAY", "WHO",
        "BOY", "DID", "ITS", "LET", "PUT", "SAY", "SHE", "TOO", "USE"],
    4: ["THAT", "WITH", "HAVE", "THIS", "WILL", "YOUR", "FROM", "THEY", "KNOW",
        "WANT", "BEEN", "GOOD", "MUCH", "SOME", "TIME", "VERY", "WHEN", "COME",
        "HERE", "JUST", "LIKE", "LONG", "MAKE", "MANY", "MORE", "ONLY", "OVER",
        "SUCH", "TAKE", "THAN", "THEM", "WELL", "WERE"],
}

MONOGRAM_ORDER = list(MONOGRAM)
BIGRAM_ORDER = list(BIGRAM)
TRIGRAM_ORDER = list(TRIGRAM)


def ordered(freq: dict) -> list:
    return sorted(freq, key=freq.get, reverse=True)


if __name__ == "__main__":
    for name, d in (("MONOGRAM", MONOGRAM), ("BIGRAM", BIGRAM), ("TRIGRAM", TRIGRAM)):
        print(f"{name} ({len(d)}): {' '.join(list(d)[:15])} ...")
