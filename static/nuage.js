anychart.onDocumentReady(async function() {
    var response = await fetch('http://127.0.0.1:5000/donnees-reponses'); // Récupération des données des réponses
    console.log(response);
    var data = await response.json();
    console.log(data.mots);

    var mots = data.mots;     // Récupération des mots
    var titre = data.titre;   // Récupération du titre
    var nuage = anychart.tagCloud(mots);     // Initialise le nuage de mots
    nuage.title(titre)   // Titre du nuage
    nuage.angles([0])                        // Angle des mots

    nuage.colorRange(true);
    nuage.colorRange().length('80%');

    nuage.container("container");            // Affichage dans la div "container"
    nuage.draw();
});