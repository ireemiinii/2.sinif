from tkinter import *
from itertools import product, starmap, islice

open_txt = open("input.txt","r")             #input dosyasını okutuyoruz
print(open_txt.read())

open_txt = open("input.txt","r")
firstline= open_txt.readline()
rows = firstline[0]     #kaça kaç olduğunu belirttik
columns = firstline[2]
rows=int(rows)
columns=int(columns)

matrixarray2d=[[0 for j in range(rows)] for i in range(columns)]
#print(matrixarray2d)           #KENDİ BOŞ LİSTEMİZİ OLUŞTURDUK.BUNU YAPMAMIZIN SEBEBİ TXT SATIR-SÜTUNLARI DEĞİŞSE BİLE KODUN ÇALIŞMASINI SAĞLAMAK

teacherlist=[]
listforgame=[]

for m in matrixarray2d: #benim 0lı 2Dli arrayım
    for n in m:
        n=str(n)
        listforgame.append(n)

    for i in range(int(rows)):  # hocanın verdiği txtyi yazdırır
        intxtline = open_txt.readline()
        #print(intxtline)
        # txtdeki input matrixin 1. satırından okumaya başlıyor
        # yapmamız gereken "1"leri matrixarray2d deki arrayımıze yazdırmak

        for j in intxtline:  # tek tek bir satırdaki sayılara bakabiliyor
            if j =="1" :
                teacherlist.append(j)
            elif j == "0" :
                teacherlist.append(j)

#print(teacherlist)        #HOCANIN TXTSİNİN LİSTESİ
#print(listforgame)        #BENİM LİSTEM

#şimdi listeleri karşılaştırma zamanı
#HOCANIN TXTSİNE BENZETECEĞİZ BÖYLECE TEK BOYUTLU LİSTEMİZ 2D LİSTE OLACAK


def indices( teacherlist, value):  #aynı liste içinde aynı elemanlardan birkaç tane olduğu için bu fonk. kullandım
    return [i for i,x in enumerate(teacherlist) if x==value]

indexsakla= indices(teacherlist, ("1"))   #tek boyut içinde 1lerin yerini bulmamı ve saklamamı sağlıyor

for i in indexsakla:
    listforgame[i]="1"
#print(listforgame)                  #bütün kod boyunca 1ler burada tutulacak

#.................................................................................................................................................
#ŞİMDİ KODLARDA KULLANACAĞIMIZ ESNEK LİSTEYİ OLUŞTURACAĞIZ:

uselist=[] #BİZİM KULLANACAĞIMIZ LİSTE
sayac=0
for i in range(len(listforgame)*2):
    if sayac == columns:
        uselist.append(listforgame[0:sayac])
        del listforgame[0:sayac]
        if listforgame==[]:
            break
    else:
        sayac+=1
print(uselist)

#................
#BURAYA KADAR TXTDEN VERİ ALIP (HER SATIR VE SUTUN İÇİN DEĞİŞKEN) KENDİ 2D LİSTEMİ YAPMIŞ OLDUM
#BÖYLECE TXTMİZ YAPILAN DEĞİŞİKLİLİKLERDEN ETKİLENMEYECEK.
#VE TXTNİN SATIR-SUTUN SAYISI DEĞİŞSE BİLE KOD HALA KULLANILABİLİR OLACAK
# .................................................................................................................................................

#ŞİMDİ PENCERİMİZİ OLUŞTURACAĞIZ

root = Tk()
frame=Frame(root)
frame.grid(row=0, column=0, sticky=N+S+E+W)

def makegrid():
    r = 0
    c=0
    for k in uselist:
        for i in k:
            if i== "1":
                Label(relief=RIDGE,bg="black",width=5,height=4).grid(row=r, column=c,sticky=N+S+E+W)
            else:
                Label(relief=RIDGE,width=5,height=4,bg="white").grid(row=r, column=c,sticky=N+S+E+W)
            c=c+1
        r = r + 1
        c=0
    mainloop()
makegrid()   #INITIALİZE FRAME

def setitem(rowIndex, colIndex, newVal):          #SETİTEM FONKSİYONU SAYESİNDE DEĞER DEĞİŞTİREBİLİRİZ
    uselist[rowIndex][colIndex] = newVal

def getnumRows():            #HOCANIN GÖNDERDİĞİ TXTDE KAÇ SATIR OLDUĞUNU DÖNDÜRÜR
    print(rows)

def getnumColums():               #HOCANIN GÖNDERDİĞİ TXTDE KAÇ SUTUN OLDUĞUNU DÖNDÜRÜR
    print(columns)

lifecell=[]                    #YAŞAYAN HÜCRELERİN İNDEXLERİNİ KAYIT ALTINA ALMAK İÇİN KULLANILIR
def indexlifecell ():
    for i in range(len(uselist)):
        for j in range(len(uselist[i])):
            if (uselist[i][j] == "1"):
                a = list((i, j))
                lifecell.append(a)


def findNeighbors(grid, x, y):                                  #HÜCRELERİN KOMŞULARINA BAKMAYA YARAYAN FONKDİYON
    xi = (0, -1, 1) if 0 < x < len(grid) - 1 else ((0, -1) if x > 0 else (0, 1))
    yi = (0, -1, 1) if 0 < y < len(grid[0]) - 1 else ((0, -1) if y > 0 else (0, 1))
    return islice(starmap((lambda a, b: grid[x + a][y + b]), product(xi, yi)), 1, None)

def degisim():                              #BİR SONRAKİ ŞEKİL OLACAK ONU BULMAMIZI SAĞLAYAN FONKSİYON
    yasayacakhucreler = []               #BU İKİ LİSTEYİ AÇMAMIZIN SEBEBİ SETİTEM FNKSİYONUNU BÜTÜN HÜCRELER
    olecekhucreler = []                  #TARANDIKTAN SONRA GERÇEKLEŞTİRİLECEK OLMASIDIR. BUNLARDA KONUMLARI SAKLAYACAĞIZ
    for i, m in enumerate(uselist):
        for j, n in enumerate(m):
            if n == "1":
                nghb = list(findNeighbors(uselist, i, j))  # find neighbors of 9
                #print(nghb)  #komşuların hangi değerde olduklarını yazdırır

                sayac = 0
                for k in nghb:
                    if k == "1":
                        sayac += 1
                # print(sayac)     # hücrelerin komşularından kaçı yaşıyorsa onun sayısını yazdırır
                if sayac == 0 or sayac == 1:
                    olecekhucreler.append([i, j])
                if sayac == 2 or sayac == 3:
                    yasayacakhucreler.append([i, j])
                if sayac >= 4:
                    olecekhucreler.append([i, j])

            if n == "0":
                nghb = list(findNeighbors(uselist, i, j))  # find neighbors of 9
                # print(nghb)  #komşuların hangi değerde olduklarını yazdırır
                yasayancell = 0
                for k in nghb:
                    if k == "1":
                        yasayancell += 1
                # print(yasayancell)     #hücrelerin komşularından kaçı yaşıyorsa onun sayısını yazdırır

                if yasayancell == 3:
                    yasayacakhucreler.append([i, j])

    print(uselist)

    for a in (yasayacakhucreler):
        setitem(a[0],a[1],"1")       #setitem fonk. ile değerleri değiştirdikten sonra konumların tutulduğu listeyi boşaltıyoruz.
    yasayacakhucreler=[]             #bunun nedeni döngünün doğruluğunu sağlamak

    for b in olecekhucreler:
        setitem(b[0],b[1],"0")       #setitem fonk. ile değerleri değiştirdikten sonra konumların tutulduğu listeyi boşaltıyoruz.
    olecekhucreler=[]                #bunun nedeni döngünün doğruluğunu sağlamak

degisim()

def newgeneration():
    istek=6                 #ne kadar generation istersek onu belirtiyoruz. başlangıç tablosu sayılmaz.
    for k in range(istek):
        makegrid()
        degisim()
        istek-=1
        if istek==0:
            break
newgeneration()

