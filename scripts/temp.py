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

# 2
"""EJEMPLO DE QUERY FUNCIONAL:
FOR v, e IN OUTBOUND SHORTEST_PATH 'words/1b7f8466f087c27f24e1c90017b829cd8208969018a0bbe7d9c452fa224bc6cc' TO 'words/8e317f8df6bcc28e25cc1bf9aa449d68679ce17b53a0cb2b2cfce188031380dc' 
        GRAPH 'relatedWords' 
        OPTIONS {
            weightAttribute: 'count',
            defaultWeight: 0
        }
        RETURN [v._key, e.from_name, e.to_name, e._key, e.count, e.inverse_count]"""

#3 modo de predicion
#~hay que hacer algo donde se importe de scipy import stats
print("Finished populating database: " + DB_NAME)