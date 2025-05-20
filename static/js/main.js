document.addEventListener('DOMContentLoaded', function () {
    // Elements
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    const themeToggle = document.getElementById('theme-toggle');
    const lightIcon = document.getElementById('light-mode');
    const darkIcon = document.getElementById('dark-mode');
    const menuItems = document.querySelectorAll('.menu-item');
    const submenuItems = document.querySelectorAll('.submenu-item');

    // Sidebar toggle
    if (sidebarToggle && sidebar && mainContent) {
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('sidebar-collapsed');
            mainContent.classList.toggle('expanded');
        });
    }

    // Menu toggle
    menuItems.forEach(item => {
        const submenu = item.querySelector('.submenu');
        const menuLink = item.querySelector('.menu-link');

        if (submenu && menuLink) {
            menuLink.addEventListener('click', function (e) {
                e.preventDefault();

                // Close other menus
                menuItems.forEach(otherItem => {
                    if (otherItem !== item) {
                        otherItem.classList.remove('active');
                    }
                });

                // Toggle current
                item.classList.toggle('active');
            });
        }
    });

    // Theme handling
    function setTheme(isDark) {
        if (isDark) {
            document.documentElement.setAttribute('data-theme', 'dark');
            darkIcon?.classList.add('active');
            lightIcon?.classList.remove('active');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.removeAttribute('data-theme');
            lightIcon?.classList.add('active');
            darkIcon?.classList.remove('active');
            localStorage.setItem('theme', 'light');
        }
    }

    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (savedTheme === 'dark') {
        setTheme(true);
    } else if (savedTheme === 'light') {
        setTheme(false);
    } else {
        setTheme(prefersDark);
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            setTheme(!isDark);
        });
    }

    // Set active submenu item based on URL
    function setActiveMenuItem() {
        const currentPath = window.location.pathname;

        submenuItems.forEach(item => {
            if (item.getAttribute('href') === currentPath) {
                item.classList.add('active');
                const parent = item.closest('.menu-item');
                if (parent) {
                    parent.classList.add('active');
                }
            }
        });
    }

    setActiveMenuItem();

    // Mobile-specific sidebar behavior
    if (window.innerWidth <= 992 && sidebar) {
        const menuLinks = document.querySelectorAll('.menu-link');

        menuLinks.forEach(link => {
            link.addEventListener('click', function () {
                if (!this.parentElement.querySelector('.submenu')) {
                    sidebar.classList.remove('sidebar-expanded');
                }
            });
        });

        document.addEventListener('click', function (event) {
            if (!sidebar.contains(event.target) && sidebar.classList.contains('sidebar-expanded')) {
                sidebar.classList.remove('sidebar-expanded');
            }
        });

        // Optional: Only expand sidebar from a specific toggle button in mobile
        sidebar.addEventListener('click', function (event) {
            if (!sidebar.classList.contains('sidebar-expanded')) {
                sidebar.classList.add('sidebar-expanded');
                event.stopPropagation();
            }
        });
    }
});
