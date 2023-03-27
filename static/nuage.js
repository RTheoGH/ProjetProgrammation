anychart.onDocumentReady(function() {
    var data = [
        {"x": "Java", "value": 12},
        {"x": "Python", "value": 56},
        {"x": "JavaScript", "value": 31},
        {"x": "C", "value": 8},
        {"x": "C++", "value": 3},
        {"x": "C#", "value": 1},
        {"x": "Ocaml", "value": 2},
    ];

    var nuage = anychart.tagCloud(data);     // Initialise le nuage de mots=
    nuage.title('Votre langage préféré ?')   // Titre du nuage
    nuage.angles([0])                        // Angle des mots

    nuage.colorRange(true);
    nuage.colorRange().length('80%');

    nuage.container("container");            // Affichage dans la div "container"
    nuage.draw();
});