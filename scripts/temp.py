# 1 modo de predicion: Funcion para recomendar siguiente palabra dada una palabra
def recommend(self, text: str) -> List[dict]:
        tokenList = self.getTokenList(text)
        tokenList = self.standardize(tokenList)
        if len(tokenList) >= self.ngramFrom:
            _from: str = self.joinStr.join(tokenList[-self.ngramFrom:])
            keyHash: str = hashlib.md5(_from.encode()).hexdigest()
            nodeCollection: str = self.getVertexCollectionName()
            paths = self.graph.traverse(
                start_vertex = nodeCollection + "/" + keyHash,
                direction = "outbound",
                strategy = "bfs",
                min_depth = 1,
                max_depth = 1
            )["paths"] # return lista de palabras conectadas, con longitud maxima de 1
            
            # ordenar los ejes porcampoinverso y sacar la mas frecuentes
            edges = [path["edges"][0] for path in paths]  
            return list(sorted([
                {
                    "token": edge["to"].split("/")[1],
                    "count": edge["count"],
                    "ngramFrom": edge["ngramFrom"],
                    "ngramTo": edge["ngramTo"],
                    "value": edge["count"] * edge["ngramFrom"] * edge["ngramTo"]
                } 
            for edge in edges], key = lambda x: x["value"], reverse = True))
        return []

    
#3 modo de predicion
#~hay que hacer algo donde se importe de scipy import stats
print("Finished populating database: " + DB_NAME)