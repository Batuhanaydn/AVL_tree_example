import math
import random

class sıralama:
    def __init__(self):
        self.data = []
        self.baslık = 0
        self.kuyruk = 0

    def bos(self):
        return self.baslık == self.kuyruk

    def push(self, data):
        self.data.append(data)
        self.kuyruk += 1
    def pop(self):
        ret = self.data[self.baslık]
        self.baslık += 1
        return ret
    
    def count(self):
        return self.kuyruk - self.baslık
    
    def print(self):
        print(self.data)
        print("**************")
        print(self.data[self.baslık : self.kuyruk])

class dugum:
    def __init__(self, data):
        self.data = data
        self.sol = None
        self.sag = None
        self.derinlik = 1

    def get_data(self):
        return self.data
    
    def get_sol(self):
        return self.sol
    
    def get_sag(self):
        return self.sag
    
    def get_derinlik(self):
        return self.derinlik

    def data_dizisi(self, data):
        self.data = data
        return
    
    def sol_dizisi(self,node):
        self.sol = node
        return

    def sag_dizisi(self, node):
        self.sag = node
        return
    
    def derinlik_dizisi(self, derinlik):
        self.derinlik = derinlik
        return

def derinlik_dizisi(node):
    if node is None:
        return 0
    return node.derinlik_dizisi()

def maksimum(a, b):
    if a > b:
        return a
    return b

def sag_donus(node):
    r"""
            A                      B
           / \                    / \
          B   C                  Bl  A
         / \       -->          /   / \
        Bl  Br                 UB Br  C
       /
     UB
    UB = dengesizlik oluşan düğüm
    """

    print("sola giden duğüm: ", node.get_data())
    ret = node.get_sol()
    node.sol_dizisi(ret.get_sag())
    ret.sag_dizisi(node)
    h1 = maksimum(derinlik_dizisi(node.get_sag()), derinlik_dizisi(node.get_sol())) + 1
    node.derinlik_dizisi(h1)
    h2 = maksimum(derinlik_dizisi(ret.get_sag()), derinlik_dizisi(ret.get_sol())) + 1
    ret.derinlik_dizisi(h2)
    return ret

def sol_donus(node):
    """
    Aynısının sola simetrik dönüşümü 
    """

    print("sağa giden düğüm: ", node.get_data())
    ret = node.get_sag()
    node.sag_dizisi(ret.get_sol())
    ret.sol_dizisi(node)
    h1 = maksimum(derinlik_dizisi(node.get_sag()), derinlik_dizisi(node.get_sol())) + 1
    node.derinlik_dizisi(h1)
    h2 = maksimum(derinlik_dizisi(ret.get_sag()), derinlik_dizisi(ret.get_sol())) + 1
    ret.derinlik_dizisi(h2)
    return ret

def lr_donus(node):      
    r"""
            A              A                    Br
           / \            / \                  /  \
          B   C   SolD   Br  C      SagD      B    A
         / \       -->  /  \         -->    /     / \
        Bl  Br         B   UB              Bl    UB  C
             \        /
             UB     Bl
    SagD = sağa dönüş  SolD = sola dönüş
    https://www.javatpoint.com/lr-rotation-in-avl-tree 
    Sitede net bir şekilde açıklanmış olsa da bizde minik bir değinelim
    lr_donus veya lr rotation = yeni bir düğüm oluşturduğumuzda düğüm sol alt ağacın 
    sağına yerleştiğinde lr rotation gerçekleşmiş olur. Buradaki düğümümüz sırasıyla sol
    ve sağ tarafın çocuğu olur.
    """
    node.sol_dizisi(sol_donus(node.get_sol()))
    return sag_donus(node)

def rl_donus(node):
    r"""
    lr rotationunun sağ alt ağacın soluna yerleşmesi durumudur.
    ayrıntılar için https://www.javatpoint.com/rl-rotation-in-avl-tree
    """
    node.sag_dizisi(sag_donus(node.get_sag()))
    return sol_donus(node)

def ekleme(node,data):
    if node is None:
        return dugum(data)
    if data < node.get_data():
        node.sol_dizisi(ekleme(node.get_sol(), data))
        if (
            derinlik_dizisi(node.get_sol()) - derinlik_dizisi(node.get_sag()) == 2
        ): 
        # Burada ağacımızda bir dengesizlik olup olmadığını tespit etmiş oluruz
            if (
                data < node.get_sol().get_data()
                # Yukarıdaki şart sağlandığında yeni düğüm, sol çocuğun sol çocuğu olur
            ):
                node = sag_donus(node)
            else:
                node = lr_donus(node)
    else:
        node.sag_dizisi(ekleme(node.get_sag(), data))
        if derinlik_dizisi(node.get_sag()) - derinlik_dizisi(node.get_sol) == 2:
            if data < node.get_sag().get_data():
                node = lr_donus(node)
            else:
                node = sol_donus(node)

    h1 = maksimum(derinlik_dizisi(node.get_sag()), derinlik_dizisi(node.get_sol())) + 1
    node.derinlik_dizisi(h1)
    return node

def get_sagMost(root):
    while root.get_sag() is not None:
        root = root.get_sag()
    return root.get_data()

def get_solMost(root):
    while root.get_sol() is not None:
        root = root.get_sol()
    return root.get_data()


def del_node(root, data):
    if root.get_data() == data:
        if root.get_sol() is not None and root.get_sag() is not None:
            bos_data = get_solMost(root.get_sol)
            root.data_dizisi(bos_data)
            root.sag_dizisi(del_node(root.get_sag(), bos_data))
        elif root.get_sol() is not None:
            root = root.get_sol()
        else:
            root = root. get_sag()
    elif root.get_data() > data:
        if root.get_sol is None:
            return root
        else:
            root.sag_dizisi(del_node(root.get_sag(), data))
    if root is None:
        return root
    
    if derinlik_dizisi(root.get_sag()) - derinlik_dizisi(root.get_sol()) == 2:
        if derinlik_dizisi(root.get_sag().get_sag()) > derinlik_dizisi(root.get_sag().get_sol()):
            root = sol_donus(root)
        else:
            root = rl_donus(root)

    elif derinlik_dizisi(root.get_sag()) - derinlik_dizisi(root.get_sol()) == -2:
        if derinlik_dizisi(root.get_sol().get_sol()) > derinlik_dizisi(root.get_sol().get_sag()):
            root = sag_donus(root)
        else:
            root = lr_donus(root)
    derinlik = maksimum(derinlik_dizisi(root.get_sag()), derinlik_dizisi(root.get_sol())) + 1
    root.derinlik_dizisi(derinlik)
    return root


class AVLtree:

    def __init__(self):
        self.root = None

    def derinlik_dizisi(self):
        # print("abb")
        return derinlik_dizisi(self.root)
    def ekleme_(self, data):
        print("Ekleme: "+ str(data))
        self.root = ekleme(self.root, data)
    def sil(self, data):
        print("Silinecek: " + str(data))
        if self.root is None:
            print("Ağac boştur")
            return
        self.root = del_node(self.root, data)
    
    def __str__(self): # Burada kullanılan self ağaca daha sezgisel hareket verir. Seviye geçişi içindir.
        cıktı = ""
        q = sıralama()
        q.push(self.root)
        katman = self.derinlik_dizisi()
        if katman == 0:
            return cıktı
        cnt = 0
        while not q.bos():
            node = q.pop()
            toplam = " " * int(math.pow(2, katman - 1))
            cıktı += toplam
            if node is None:
                cıktı += "*"
                q.push(None)
                q.push(None)
            else:
                cıktı += str(node.get_data())
                q.push(node.get_sol())
                q.push(node.get_sag())
            cıktı += katman
            cnt += 1
            for i in range(100): # değişkenlik gösterebilir
                if cnt == math.pow(2, i) - 1:
                    katman -= 1
                    if katman == 0:
                        cıktı += "\n***************"
                        return cıktı
                    cıktı += "\n"
                    break
        cıktı += "\n**************"
        return cıktı

def test():
    import doctest

    doctest.testmod()


if __name__ == "__main__":
    test()
    t = AVLtree()
    liste = list(range(10))
    random.shuffle(liste)
    for i in liste:
        t.ekleme_(i)
        print(str(t))
    random.shuffle(liste)
    for i in liste:
        t.sil(i)
        print(str(t))

# Kod https://github.com/TheAlgorithms, https://www.javatpoint.com/avl-tree ve https://en.wikipedia.org/wiki/AVL_tree yardımıyla yazılmıştır.

        













