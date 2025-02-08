document.addEventListener("DOMContentLoaded", function() {
    const filterForm = document.getElementById("filter-form");
    const resetBtn = document.querySelector(".reset-btn");

    filterForm.reset();

    resetBtn.addEventListener("click", function () {
        filterForm.reset();

        const url = new URL(window.location.href);
        url.search = "";
        window.history.replaceState({}, document.title, url);

        window.location.href = url;
    })
});

// $(function() {
//     $("#id_start_date").datepicker({
//         changeMonth: true,
//         changeYear: true,
//         yearRange: "2000:2030",
//         maxDate: new Date(),
//         onSelect: function (dateText, inst) {
//             var formattedDate = $.datepicker.formatDate('M dd, yy', $(this).datepicker('getDate'));
//             $(this).val(formattedDate);
//         }
//     });
//     $("#id_end_date").datepicker({
//         changeMonth: true,
//         changeYear: true,
//         yearRange: "2000:2030",
//         maxDate: new Date(),
//         onSelect: function (dateText, inst) {
//             var formattedDate = $.datepicker.formatDate('M dd, yy', $(this).datepicker('getDate'));
//             $(this).val(formattedDate);
//         }
//     });
// });
//