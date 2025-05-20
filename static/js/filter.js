/**
 * Date range filtering functionality for tables
 */
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on a page with date filters
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
    const applyFilterButton = document.getElementById('apply-filter');
    const resetFilterButton = document.getElementById('reset-filter');
    
    if (startDateInput && endDateInput && applyFilterButton && resetFilterButton) {
        // Initialize with current date range
        const today = new Date();
        const oneMonthAgo = new Date();
        oneMonthAgo.setMonth(oneMonthAgo.getMonth() - 1);
        
        // Format dates for input fields (YYYY-MM-DD)
        endDateInput.value = formatDate(today);
        startDateInput.value = formatDate(oneMonthAgo);
        
        // Clear any existing search functions to avoid duplicates
        if ($.fn.dataTable.ext.search.length > 0) {
            // Remove all custom search functions
            $.fn.dataTable.ext.search.splice(0, $.fn.dataTable.ext.search.length);
        }
        
        // Add our date range filter function
        $.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
            if (settings.nTable.id !== 'milestone-table') {
                return true; // Only apply to orders table
            }
            
            const dateStr = data[2]; // Date is in the third column (index 2)
            
            // Exit early if no date in this row or no filter set
            if (!dateStr) {
                return true;
            }
            
            const startDateValue = startDateInput.value;
            const endDateValue = endDateInput.value;
            
            if (!startDateValue && !endDateValue) {
                return true;
            }
            
            // Parse the date in the format displayed in the table (YYYY-MM-DD)
            const rowDate = new Date(dateStr);
            
            // Check if the date is within the range
            let inRange = true;
            
            if (startDateValue) {
                const startDate = new Date(startDateValue);
                inRange = inRange && rowDate >= startDate;
            }
            
            if (endDateValue) {
                const endDate = new Date(endDateValue);
                // Set time to end of day for end date
                endDate.setHours(23, 59, 59, 999);
                inRange = inRange && rowDate <= endDate;
            }
            
            return inRange;
        });
        
        // Set up the "Apply Filter" button
        applyFilterButton.addEventListener('click', function() {
            const table = $('#milestone-table').DataTable();
            table.draw(); // Apply filter by redrawing the table
        });
        
        // Set up the "Reset" button
        resetFilterButton.addEventListener('click', function() {
            const today = new Date();
            const oneMonthAgo = new Date();
            oneMonthAgo.setMonth(oneMonthAgo.getMonth() - 1);
            
            // Reset input values
            endDateInput.value = formatDate(today);
            startDateInput.value = formatDate(oneMonthAgo);
            
            // Redraw the table with the default filters
            const table = $('#milestone-table').DataTable();
            table.draw();
        });
    }
    
    /**
     * Format date as YYYY-MM-DD for input fields
     */
    function formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }
});