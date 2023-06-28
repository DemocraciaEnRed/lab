from googlesearch import Search


class Google:

    def __init__(self, full_name: str):

        try:
            self.results = Search(full_name, number_of_results=10).results
        except Exception as e:
            self.results = None
            print(f"{full_name} {e}")
        
        self.twitter_account = self.get_for("https://twitter.com")
        self.instagram_account = self.get_for("instagram.com")
        self.facebook_account = self.get_for("facebook.com")
        self.wikipedia_page = self.get_for("wikipedia.org")

    def get_for(self, point):
    
        # Filtrar el elemento que contiene la referencia
        if not self.results:
            return
        any_results = next((result for result in self.results if point in result.url), None)
        if any_results:
            if any_results.url:
                return any_results.url.split('?')[0]

