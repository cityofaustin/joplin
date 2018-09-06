export default function () {
    $('.js-toggle-active-panel').on('click', function () {
        $('.js-toggle-active-panel').removeClass('coa-sidebar-button--active');
        $(this).addClass('coa-sidebar-button--active');
    })
}