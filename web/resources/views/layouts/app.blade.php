<!DOCTYPE html>
<html lang="en">
@include('partials.head')
<title>@yield('title')</title>

<!-- Mirrored from adminlte.io/themes/v3/ by HTTrack Website Copier/3.x [XR&CO'2014], Mon, 20 Jan 2025 06:07:51 GMT -->
<body class="hold-transition sidebar-mini layout-fixed">
<div class="wrapper">

    <!-- Preloader -->
@include('partials.preloader')
    <!-- Navbar -->
@include('partials.navbar')
    <!-- /.navbar -->

    <!-- Main Sidebar Container -->
@include('partials.sidebar')
    <!-- Content Wrapper. Contains page content -->
    <div class="content-wrapper">
        <!-- Content Header (Page header) -->
        <div class="content-header">
            <div class="container-fluid">
                <div class="row mb-2">

                    <div class="col-sm-6">
                        <ol class="breadcrumb float-sm-right">
                            <li class="breadcrumb-item"><a href="#">Home</a></li>
                            <li class="breadcrumb-item active">@yield('breadcrumbs')</li>
                        </ol>
                    </div><!-- /.col -->
                </div><!-- /.row -->
            </div><!-- /.container-fluid -->
        </div>
        <!-- /.content-header -->

        <!-- Main content -->
        <section class="content">
            <div class="container-fluid">

               @yield('content')
            </div><!-- /.container-fluid -->
        </section>
        <!-- /.content -->
    </div>
    <!-- /.content-wrapper -->
@include('partials.footer')
    <!-- Control Sidebar -->
@include('partials.controlsidebar')
    <!-- /.control-sidebar -->
</div>
<!-- ./wrapper -->
@include('partials.scripts')
</body>

<!-- Mirrored from adminlte.io/themes/v3/ by HTTrack Website Copier/3.x [XR&CO'2014], Mon, 20 Jan 2025 06:09:29 GMT -->
</html>
