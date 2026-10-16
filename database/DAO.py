from database.DB_connect import DBConnect
from model.film import Film
from model.attore import Attore


class DAO:
    @staticmethod
    def getFilm(rMin, rMax):
        """
        Film con valutazione media nell'intervallo [rMin, rMax] (estremi inclusi).
        Restituisce una lista di oggetti Film.
        """
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            print("Connessione fallita")
            return results

        cursor = conn.cursor(dictionary=True)
        query = """SELECT m.id AS id, m.title AS titolo, m.year AS anno, r.avg_rating AS voto
                   FROM movie m, ratings r
                   WHERE m.id = r.movie_id
                     AND r.avg_rating BETWEEN %s AND %s"""
        cursor.execute(query, (rMin, rMax))
        for row in cursor:
            results.append(Film(row["id"], row["titolo"], row["anno"], float(row["voto"])))

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getNodi(rMin, rMax):
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            print("Connessione fallita")
            return results

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT n.id AS id, n.name AS nome, n.date_of_birth AS data
                FROM names n, role_mapping r, ratings ra
                WHERE n.id = r.name_id AND r.category IN ('actor','actress'  ) AND 
                r.movie_id = ra.movie_id AND ra.avg_rating BETWEEN %s AND %s
                ORDER BY n.id, n.name
                
                """
        cursor.execute(query, (rMin, rMax))
        for row in cursor:
            results.append(Attore(row["id"], row["nome"], row["data"]))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getCoppia():
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            print("Connessione fallita")
            return results

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT r.name_id AS idA,r.movie_id AS idF
                FROM  role_mapping r
                WHERE r.category IN ('actor','actress'  )
                """
        cursor.execute(query)
        for row in cursor:
            results.append((row["idA"], row["idF"]))
        cursor.close()
        conn.close()
        return results

