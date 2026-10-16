import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def _errore(self, msg):
        self._view._txt_result.controls.append(ft.Text(msg, color="red"))
        self._view.update_page()

    # -------------------- PUNTO 1 --------------------

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()

        try:
            rMin = float(self._view._txtRatingMin.value)
            rMax = float(self._view._txtRatingMax.value)
        except (ValueError, TypeError):
            self._errore("I rating devono essere numeri!")
            return
        if rMin > rMax:
            self._errore("Il rating minimo non può essere maggiore del massimo!")
            return

        self._model.buildGraph(rMin, rMax)
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di vertici: {self._model.getNumNodi()}"))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        # riempio il dropdown degli attori (punto 2)
        self._view._ddActor.options.clear()
        self._view._ddActor.value = None
        for a in self._model.getNodiOrdinati():
            self._view._ddActor.options.append(ft.dropdown.Option(key=a.id, text=a.name))

        self._view.update_page()

    def handleStampaInfo(self, e):
        self._view._txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        # a. grado maggiore
        at, grado = self._model.getGradoMax()
        self._view._txt_result.controls.append(
            ft.Text(f"Attore con grado maggiore: {at} (grado: {grado})"))

        # b. somma pesi incidenti massima
        attore, peso = self._model.getIncidenti()
        self._view._txt_result.controls.append(
            ft.Text(f"Attore con somma pesi incidenti massima: {attore} (somma: {peso})"))

        # d. ed e. più giovane e più anziano
        giovane, anziano = self._model.getGiovaneAnziano()
        if giovane is None:
            self._view._txt_result.controls.append(
                ft.Text("Nessun attore del grafo ha la data di nascita"))
        else:
            self._view._txt_result.controls.append(
                ft.Text(f"Attore più giovane: {giovane} (nato il {giovane.date_of_birth})"))
            self._view._txt_result.controls.append(
                ft.Text(f"Attore più anziano: {anziano} (nato il {anziano.date_of_birth})"))

        # c. 5 archi di peso maggiore
        self._view._txt_result.controls.append(ft.Text(""))
        self._view._txt_result.controls.append(ft.Text("Top 5 archi con peso maggiore:"))
        for i, (n1, n2, p) in enumerate(self._model.get5(), start=1):
            self._view._txt_result.controls.append(ft.Text(f"{i}. {n1} -- {n2} (peso: {p})"))

        self._view.update_page()

    # -------------------- PUNTO 2 --------------------

    def handleTrovaGruppo(self, e):
        self._view._txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        idAttore = self._view._ddActor.value
        if idAttore is None:
            self._errore("Selezionare un attore di partenza!")
            return
        start = self._model._idMap[idAttore]

        try:
            n = int(self._view._txtInN.value)
        except (ValueError, TypeError):
            self._errore("N deve essere un numero intero!")
            return
        if n < 1:
            self._errore("N deve essere almeno 1!")
            return

        gruppo, totFilm = self._model.getGruppo(start, n)

        if len(gruppo) == 0:
            self._errore(f"Nessun gruppo di {n} attori ad albero partendo da {start}")
            return

        self._view._txt_result.controls.append(ft.Text(f"Gruppo trovato partendo da {start}:"))
        for a in sorted(gruppo, key=lambda x: x.name):
            self._view._txt_result.controls.append(
                ft.Text(f"{a.name} - film: {len(a.film)}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero di attori: {len(gruppo)}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero complessivo di film: {totFilm}"))
        self._view.update_page()