/*
 <script>
    $(document).ready(function () {
        let formIndex = {{ forms_set.total_form_count |default:"0" }};

        $('#add-form').click(function () {
            let formTemplate = $('.formset-item:first').clone(true);
             console.log("Bouton cliqué !");
            alert("Le JS fonctionne !");

            // Met à jour les noms et ids des champs
            formTemplate.find(':input').each(function () {
                let name = $(this).attr('name');
                if (name) {
                    let newName = name.replace(/\d+/, formIndex);
                    $(this).attr('name', newName).attr('id', 'id_' + newName).val('');
                }
            });

            // Ajoute le nouveau formulaire
            $('#formset-container').append(formTemplate);

            // Mets à jour le total des formulaires
            let totalForms = $('#id_form-TOTAL_FORMS');
            totalForms.val(parseInt(totalForms.val()) + 1);

            formIndex++;
        });
    });
</script>
*/

