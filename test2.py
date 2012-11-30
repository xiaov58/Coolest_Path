#

class ken:
    def __init__(self):   
        self.a = 1
    def run(self):
        g = gen (self)
        g.run()
        
class gen:
    def __init__(self, ken):   
        self.ken = ken
    def run(self):
        self.ken.a = 2
   
def main():   
    k = ken()
    k.run()
    print k.a

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
