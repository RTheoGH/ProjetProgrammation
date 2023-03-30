anychart.onDocumentReady(async function() {
    var response = await fetch('http://127.0.0.1:5000/donnees-reponses'); // Récupération des données des réponses
    console.log(response);
    var data = await response.json();

    var nomProf = document.getElementById('nomDuProf').textContent; // Récupération du nom du prof depuis la page HTML
    var mots = data[nomProf][0].mots;        // Récupération des mots du nuage
    console.log(mots);
    var titre = data[nomProf][0].titre;      // Récupération du titre du nuage
    console.log(titre);
    var nuage = anychart.tagCloud(mots);     // Initialise le nuage de mots
    nuage.title(titre)   // Titre du nuage
    nuage.angles([0])                        // Angle des mots

    nuage.colorRange(true);
    nuage.colorRange().length('80%');

    nuage.container("container");            // Affichage dans la div "container"
    nuage.draw();
});