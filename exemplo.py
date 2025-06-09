def voto(idade):
    if idade < 16:
        print("Inapto for votar!")
    else:
        if idade >= 16 and idade < 18:
            print("voto facultativo")

        elif idade >= 18 and idade < 64:
            print("voto obrigatório")

        else:
            print("voto facultativo")

if __name__ == "__main__":
    idade = 14
    print(f"idade from {idade} anos")
    voto(idade)

    idade = 17
    print(f"idade from {idade} anos")
    voto(idade)

    idade = 25
    print(f"idade from {idade} anos")
    voto(idade)

    idade = 66
    print(f"idade from {idade} anos")
    voto(idade)