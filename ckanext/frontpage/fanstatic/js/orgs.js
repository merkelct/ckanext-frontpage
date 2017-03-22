$(document).ready(function() {
    //remove the blank selectedOrg option that can show up if Update Config is called with no
    //featured orgs selected
    $(".selectedOrg[value='']").remove()

    $("select[name='featured_orgs'] > option").each(function(){
        var optionValue = $(this).attr('value');

        $("select[name='new-featured-orgs'] > option").each(function(){

            //remove already selected orgs from the available list
            if ($(this).attr('value') == optionValue){
                $(this).remove();
            }
        });

    });

    $("select[name='new-featured-orgs']").on('click', 'option', function() {
        var opt = $(this).clone();
        opt.removeClass("availableOrg");
        opt.addClass("selectedOrg");
        opt.prop("selected",true);

        $("select[name='featured_orgs']").append(opt);
        $(this).remove();
    });

    $("select[name='featured_orgs']").on('click', 'option', function() {
        var opt = $(this).clone();
        opt.removeClass("selectedOrg");
        opt.addClass("availableOrg");
        opt.prop("selected",false);

        $("select[name='new-featured-orgs']").append(opt);
        $(this).remove();

        $("select[name='featured_orgs'] > option").each(function(){
            $(this).prop("selected", true);
        });
    });
});
