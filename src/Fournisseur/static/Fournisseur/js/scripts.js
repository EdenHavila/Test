

    $(document).ready(function() {

          $('#id_biens').closest('div').hide();
          $('#id_services').closest('div').hide();
        // Lorsqu'on sélectionne le type de fournisseur (Bien ou Service)
        $('#id_specialite').change(function() {
            var type = $(this).val();  // "bien" ou "service"
             console.log("Type sélectionné : " + type);
            // Masquer les champs biens et services initialement
            console.log("Affiche champs manuellement");
            $('#id_biens').closest('div').hide();
            $('#id_services').closest('div').hide();

            if (type) {

                // En fonction du type sélectionné, on charge la liste correspondante via AJAX
                $.ajax({
                    url: '{% url "getBiensOrServicesURL" %}', getBiensOrServicesURL // URL pour récupérer les biens/services'{% url "Fournisseur:get-biens-or-services" %}'
                    data: {
                        'specialite': type
                    },
                    dataType: 'json',

                    success: function(data) {
                        // Afficher le champ approprié
                        if (type == 'Bien') {
                            $('#id_biens').closest('div').show();
                            $('#id_services').closest('div').hide();
                            // Remplir le select "biens" avec les données renvoyées
                            $('#id_biens').empty();
                            $.each(data, function(index, item) {
                                $('#id_biens').append($('<option>', {
                                    value: item.id,
                                    text: item.designation
                                }));
                            });
                        } else if (type == 'Service') {
                            $('#id_services').closest('div').show();
                            $('#id_biens').closest('div').hide();
                            // Remplir le select "services" avec les données renvoyées
                            $('#id_services').empty();
                            $.each(data, function(index, item) {
                                $('#id_services').append($('<option>', {
                                    value: item.id,
                                    text: item.designation
                                }));
                            });
                        }
                    }
                });
            }
        });
    });








































<script type="text/javascript">
    $(document).ready(function() {

          $('#id_bien').closest('div').hide();
          $('#id_service').closest('div').hide();
        // Lorsqu'on sélectionne le type de fournisseur (Bien ou Service)
        $('#id_type').change(function() {
            var type = $(this).val();  // "bien" ou "service"
             console.log("Type sélectionné : " + type);
            // Masquer les champs biens et services initialement
            $('#id_bien').closest('div').hide();
            $('#id_service').closest('div').hide();

            if (type) {


                        // Afficher le champ approprié
                        if (type == 'Bien') {
                            $('#id_bien').closest('div').show();
                            $('#id_service').closest('div').hide();


                        } else if (type == 'Service') {
                            $('#id_service').closest('div').show();
                            $('#id_bien').closest('div').hide();


                        }
                    }
                });
            }

    });
</script>










<script type="text/javascript">
    $(document).ready(function () {

        // 1. Fonction pour afficher le bon champ selon le type sélectionné
        function toggleFields(container, selectedType) {
            const bienField = container.find('.field-bien').closest('div');
            const serviceField = container.find('.field-service').closest('div');

            bienField.hide();
            serviceField.hide();

            if (selectedType === 'Bien') {
                bienField.show();
            } else if (selectedType === 'Service') {
                serviceField.show();
            }
        }

        // 2. Applique toggleFields sur tous les champs .type-selector au chargement
        $('.type-selector').each(function () {
            const container = $(this).closest('.formset-item');
            toggleFields(container, $(this).val());
        });

        // 3. Écoute dynamique : changement de type (même pour les futurs champs ajoutés)
        $(document).on('change', '.type-selector', function () {
            const container = $(this).closest('.formset-item');
            toggleFields(container, $(this).val());
        });

        // 4. Ajouter dynamiquement une ligne de formulaire
        let formIndex = parseInt($('#id_form-TOTAL_FORMS').val());

        $('#add-form').click(function () {
            const formTemplate = $('.formset-item:first').clone(true);

            // Nettoyage et renommage des champs
            formTemplate.find(':input').each(function () {
                const name = $(this).attr('name');
                const id = $(this).attr('id');
                if (name) {
                    const newName = name.replace(/\d+/, formIndex);
                    const newId = id.replace(/\d+/, formIndex);
                    $(this).attr({ name: newName, id: newId }).val('');
                }
            });

            // Cacher les champs bien / service au départ
            formTemplate.find('.field-bien').closest('.form-group').hide();
            formTemplate.find('.field-service').closest('.form-group').hide();

            // Ajouter le nouveau bloc au DOM
            $('#formset-container').append(formTemplate);

            // Mettre à jour le total des formulaires
            $('#id_form-TOTAL_FORMS').val(formIndex + 1);
            formIndex++;
        });
         // Suppression d'une ligne
        $(document).on('click', '.delete-form', function () {
            // Supprime la ligne correspondante
            $(this).closest('.formset-item').remove();

            // Mets à jour le total des formulaires
            let totalForms = $('#id_form-TOTAL_FORMS');
            totalForms.val(parseInt(totalForms.val()) - 1);
        });
    });
</script>