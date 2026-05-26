<?php
/**
 * PhishPulse - Dashboard Header
 * Version: 1.0
 * Author: ATHEX BLACK HAT
 */

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Check login
if (!isset($_SESSION['logged_in']) && basename($_SERVER['PHP_SELF']) !== 'index.php') {
    header('Location: index.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo DASHBOARD_TITLE; ?> v<?php echo DASHBOARD_VERSION; ?></title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🔴</text></svg>">
    <style>
        /* Included inline for single-file portability */
        <?php include 'assets/css/dashboard.css'; ?>
    </style>
</head>
<body>
    
    <!-- Particle Background -->
    <div id="particles"></div>
    
    <!-- Main Container -->
    <div class="main-container">
        
        <!-- Top Navigation -->
        <nav class="top-nav">
            <div class="nav-brand">
                <span class="brand-icon">🔴</span>
                <span class="brand-text"><?php echo TOOL_NAME; ?></span>
                <span class="brand-version">v<?php echo DASHBOARD_VERSION; ?></span>
            </div>
            <div class="nav-links">
                <a href="#dashboard" class="nav-link active" data-tab="dashboard">📊 Dashboard</a>
                <a href="#sessions" class="nav-link" data-tab="sessions">👥 Sessions</a>
                <a href="#analytics" class="nav-link" data-tab="analytics">📈 Analytics</a>
                <a href="#settings" class="nav-link" data-tab="settings">⚙️ Settings</a>
                <a href="?logout=1" class="nav-link logout">🚪 Logout</a>
            </div>
            <div class="nav-status">
                <span class="live-dot"></span>
                <span class="live-text">LIVE</span>
            </div>
        </nav>