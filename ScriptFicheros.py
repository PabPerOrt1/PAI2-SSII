import os, random, secrets

def main():
    i = 0
    while i < 1001:
        file = open('./Ficheros_de_Prueba/Prueba' + str(i) + '.txt', "w")
        file.write(str(random.randrange(50000, 70000, 4)))
        file.write("\n" + str(random.randrange(50000, 70000, 4))) 
        file.write("\n" + str(random.randrange(1,9999,1)))
        file.write("\n" + str(secrets.randbelow(9999)))
        file.close()
        i +=1
if __name__ == '__main__':
    main()