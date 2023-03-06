function demandePlusReponse() {
    fetch('/plusDeReponse') /* Utilisation de l'API Fetch pour */
        .then(response => response.text()) /*envoyer une requête GET à /plusDeReponse */
        .then(data => {
            $(".nouveauBouton").append(data); /* Ajout texte de la réponse */
        }); /* à un élément ayant la classe */
} /* 'nouveauBouton' */

function supprimerBouton(id) {
    for (let i = 0; i < 3; i++) {
        fetch('/supprimer_bouton', { /* Envoi d'une requête DELETE à la route  */
            method: 'DELETE',
            /* '/supprimer_bouton' avec un objet JSON */
            body: JSON.stringify({ /* contenant l'id en paramètre */
                'id': id
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }); /* Suppression de l'élément HTML */
        $("#" + id).remove(); /* ayant pour id l'id passé en paramètre */
    }
    visualiser()
}

function visualiser() {
    // 
    let textAll = $("textarea, input:text")
    //let textAll = $("textarea"); /*Variable textAll qui recupere le contenu de toutes les textarea*/
    //textAll.append($("input"))
    console.log(textAll);
    let texte = "<h2>Enoncé :</h2>";
    textAll.each(function(index) { /* Pour chaque zone de texte */
        // console.log(this);
        if (index == 0) { /* Si c'est la premiere zone de texte (énoncé)*/
            texte += converter.makeHtml($(this).val());
            texte += "<hr/><h2>Réponses :</h2>";
        } else { /* Pour les réponses */
            texte += "<div class='repLi'>\
                <div class='repCo'><input type='checkbox'/></div>\
                <div class='repCo'> " + converter.makeHtml($(this).val()) + "</div>\
                </div>";
        }
    })
    $(".visuel").html(texte); /* Remplacement du contenu HTML (jQuery) de l'élément ayant */
    MathJax.typeset(); /* la classe 'visuel' avec la valeur de texte */
    hljs.highlightAll();
}

function Question_Numerique() {
    document.querySelector('#Quest_QCM').disabled = true;
    document.querySelector('#Quest_QCM').hidden = true;
    document.querySelector('#Rep_num').disabled = false;
    document.querySelector('#Rep_num').hidden = false;
    document.querySelector('#Quest_Num').disabled = true;
    document.querySelector('#Quest_Num').hidden = true;
    document.querySelector('#Rep_num').setAttribute("required", "");
}

function Question_QCM() {
    document.querySelector('#demandereponse').disabled = false;
    document.querySelector('#demandereponse').hidden = false;
    document.querySelector('#Quest_Num').disabled = true;
    document.querySelector('#Quest_Num').hidden = true;
    document.querySelector('#Quest_QCM').disabled = true;
    document.querySelector('#Quest_QCM').hidden = true;
}

/* EN TRAVAUX */
function downloadHtml() {
    // Récupération du code HTML à enregistrer
    var html = "<html><head><title>Mon titre</title></head><body><h1>Bienvenue !</h1></body></html>";

    // Création d'un objet Blob contenant le code HTML
    var blob = new Blob([html], {type: "text/html;charset=utf-8"});

    // Création d'un objet URL pour le fichier
    var url = URL.createObjectURL(blob);

    // Création d'un élément <a> pour le téléchargement du fichier
    var a = document.createElement("a");
    a.href = url;
    a.download = "monfichier.html";

    // Ajout de l'élément <a> au DOM et simulation du clic pour le téléchargement
    document.body.appendChild(a);
    a.click();

    // Nettoyage de l'objet URL
    URL.revokeObjectURL(url);
}