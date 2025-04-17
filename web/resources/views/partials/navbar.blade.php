<nav class="main-header navbar navbar-expand navbar-white navbar-light">
    <!-- Left navbar links -->
    <ul class="navbar-nav">
        <li class="nav-item">
            <a class="nav-link" data-widget="pushmenu" href="#" role="button"><i class="fas fa-bars"></i></a>
        </li>
        <li class="nav-item d-none d-sm-inline-block">
            <a href="/" class="nav-link">Home</a>
        </li>
    </ul>

    <!-- Right navbar links -->
    <ul class="navbar-nav ml-auto">
        <!-- Profile Dropdown -->
        <li class="nav-item dropdown">
            <a class="nav-link" data-toggle="dropdown" href="#" role="button" aria-expanded="false">
                <i class="fas fa-user-circle"></i>
                <span class="ml-1">{{ session('user_name') ?? 'Profile' }}</span>
            </a>
            <div class="dropdown-menu dropdown-menu-right">
                <a href="/profile" class="dropdown-item">
                    <i class="fas fa-user mr-2"></i> My Profile
                </a>
                <div class="dropdown-divider"></div>
                <form action="/logout" method="post" class="text-center">
                    @csrf
                    <button type="submit" class="btn btn-outline-secondary btn-block py-2 rounded">
                        <i class="fas fa-sign-out-alt mr-2"></i> Logout
                    </button>
                </form>
            </div>
        </li>
    </ul>
</nav>
