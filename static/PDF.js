async function telechargementMultiple(anonyme){
    let nom = document.getElementById("nom").value;
    var response = await fetch('http://127.0.0.1:5000/download-delete',{
        method:'POST',
        body:new URLSearchParams({"nom":nom})
    });
    var data = await response.json();
    console.log(data);

    var titre = data[0];     // Récupération du titre des contrôles
    console.log(titre);

    const doc = new jsPDF({anonyme});

    // Entête pour chaque sujet :
    var pivot = 95;
    function entete(){
        const months = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"];
        const d = new Date();
        doc.addImage('data:image/jpeg;base64,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', 'JPEG', 5, 5, 20, 20);;
        doc.setFontSize(25);
        doc.text(30, 15, 'Examen');
        doc.setFontSize(18);
        doc.text(30,25, d.getDate()+' '+months[d.getMonth()]+' '+d.getFullYear());
        doc.line(0, 35, 220, 35);
        doc.text(5,45,titre);
        if (anonyme){
            var X = 10;
            var Y = 65;
            doc.setFontSize(14);
            doc.text(5,55,"Coder votre numéro d'anonymat :")
            doc.setFontSize(11);
            for(let i=0;i<10;i++){
                Y = 65;
                doc.text(X+1,Y-3,i.toString())
                for(let j=0;j<6;j++){
                    doc.rect(X,Y,5,5);
                    Y+=7;
                }
                X+=7;
            }
            doc.setFontSize(14);
            doc.text(115,55,"Coller votre étiquette d'anonymat ici :");
            doc.rect(115,60,90,25);
            pivot = 115;
        }else{
            doc.setFontSize(14);
            doc.text(5,60,'Nom :');
            doc.rect(5, 62, 50, 10);
            doc.text(65,60,'Prénom :');
            doc.rect(65, 62, 50, 10);
            doc.text(125,60,"Numéro d'étudiant :");
            doc.rect(125, 62, 70, 10);
            pivot = 85;
        }
        doc.setLineWidth(2);
        doc.line(0, pivot, 220, pivot);
        pivot+=10;
        doc.setLineWidth(0);
    }
    
    // Affichage

    let controles = data.slice(1,data.length); // Récupération des données sauf le titre
    Array.from(controles).forEach((controle) => {    // Pour chaque sujet
        console.log(controle);
        entete();
        Array.from(controle).forEach((question) => {   // Pour chaque question des sujets
            doc.setFontSize(18);
            doc.text(5,pivot,question[0]);   // Récupération de l'énoncé de la question
            pivot+=10;
            let reponses = question[1];      // Récupération des réponses de la question
            if(reponses.length>1){     // Si plusieurs réponses (choix multiples)
                Array.from(reponses).forEach((reponse) => {  // Pour chaque réponse des questions
                    doc.setFontSize(15);
                    doc.text(15,pivot+10,reponse);
                    doc.rect(5,pivot+6,5,5);
                    pivot+=10;
                    if (pivot >= 260) {  // Si on arrive en bas de page, on passe à la page suivante
                        doc.addPage();
                        pivot = 30;
                    }
                });
            }else{   // Si une seule réponse (numérique)
                doc.rect(5,pivot+6,100,20);
                pivot+=30;
                if (pivot >= 270) {   // Si on arrive en bas de page, on passe à la page suivante
                    doc.addPage();
                    pivot = 20;
                }
            }
            doc.line(0, pivot+5, 220, pivot+5);  // Ligne pour séparer chaque question
            pivot+=15;
        })
        doc.addPage();   // Saut de page entre chaque sujet
    });
    var nombreDePages = doc.internal.getNumberOfPages(); // Récupération du nombre de pages du fichier
    for(var i=1;i<=nombreDePages;i++){  // Numérotage de chaque page
        doc.setPage(i);
        doc.text(106,290,String(i));
    }
    doc.deletePage(nombreDePages); // Suppression de la dernière page qui est vide
    doc.save("Examen.pdf");
}