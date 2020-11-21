import pandas as pd


# Wczytanie danych
df = pd.read_csv("test.csv")


# Wypisanie liczby wszystkich osób urodzonych po 1999-12-31
print(
    f"Ilosc osob urodzonych po 1999-12-31: {df.data_urodzenia[df.data_urodzenia > '31.12.1999'].count()}"
)

# Wypisanie wszystkich imion żeńskich
print(f"Wszystkie imiona zenskie jako set {set(df.imie[df.imie.str.endswith('a')])}")
