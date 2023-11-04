

from vslib.error import Error
class Reader():
    
    def __init__(self, file):
        self.file = file
        self.x_list =[]
        self.y_list = []

    def read_csv_file(self):
        
        line = self.file.readline()
        if line == '':
            raise Error('empty file or missing points')
        n = line.rstrip().split(",")
        
        if len(n) != 2 :
            raise Error('incorrect data')
        
        if n[0] == '' or n[1] == '':
            raise Error('missing data')
        

        try:
            float(n[0]) and float(n[1])
        except ValueError:
            raise Error('wrong data, ValueError')
            
        self.x_list.append(float(n[0]))
        self.y_list.append(float(n[1]))
        k = 0
        while line != '':
            line = self.file.readline()
            if line == '' and k == 0:
                raise Error('not enough data')
            n = line.rstrip().split(",")
              
            if n[0] != '':
                
                try:
                    float(n[0]) and float(n[1])
                except ValueError:
                    raise Error('wrong data, ValueError')    

                if len(n) != 2:
                    raise Error('incorrect data')
                
                if n[1] == '':
                    raise Error('missing data')
                    
                self.x_list.append(float(n[0]))
                self.y_list.append(float(n[1]))

            k = k+1
            
        return (self.extract_distances(self.x_list), self.extract_distances(self.y_list),max(self.x_list),min(self.x_list),max(self.y_list),min(self.y_list))
        
    def extract_distances(self,list):
        
        return max(list)-min(list)
    
    def read_line(self):
        return self.file.readline()
        