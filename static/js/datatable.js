/**
 * Configure DataTables with custom settings for the application
 */
function initializeDataTable(tableId) {
    const isDarkTheme = document.documentElement.getAttribute('data-theme') === 'dark';
    
    return $(`#${tableId}`).DataTable({
        scrollX:true,
        scrollY:true,
        responsive:false,
        pageLength: 10,
        lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
        dom: '<"top"lf>rt<"bottom"ip><"clear">',
        language: {
            search: "_INPUT_",
            searchPlaceholder: "Search...",
            lengthMenu: "Show _MENU_ entries",
            info: "Showing _START_ to _END_ of _TOTAL_ entries",
            paginate: {
                first: '<i class="fas fa-angle-double-left"></i>',
                previous: '<i class="fas fa-angle-left"></i>',
                next: '<i class="fas fa-angle-right"></i>',
                last: '<i class="fas fa-angle-double-right"></i>'
            }
        },
        initComplete: function() {
            // Add custom filtering controls if needed
            const api = this.api();
            
            // Add class to improve styling
            $('.dataTables_wrapper').addClass('custom-datatable');
            
            // Apply theme-specific styling
            applyThemeStyling(isDarkTheme);
        }
    });
}

/**
 * Apply theme-specific styling to DataTables elements
 */
function applyThemeStyling(isDarkTheme) {
    if (isDarkTheme) {
        $('.dataTables_wrapper .dataTables_filter input').css({
            'background-color': '#2d2d2d',
            'color': '#f0f0f0',
            'border-color': '#444444'
        });
        
        $('.dataTables_wrapper .dataTables_length select').css({
            'background-color': '#2d2d2d',
            'color': '#f0f0f0',
            'border-color': '#444444'
        });
    }
}

/**
 * Re-apply theme styling when theme changes
 */
function updateDataTableTheme() {
    const isDarkTheme = document.documentElement.getAttribute('data-theme') === 'dark';
    applyThemeStyling(isDarkTheme);
}

document.addEventListener('DOMContentLoaded', function(){
    initializeDataTable('all-runtime-table');
    initializeDataTable('milestone-table');
})

// Listen for theme changes
document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            // Small delay to ensure the theme has changed
            setTimeout(updateDataTableTheme, 100);
        });
    }
});
