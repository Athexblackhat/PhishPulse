        <!-- Footer -->
        <footer class="dashboard-footer">
            <div class="footer-left">
                <span class="footer-brand"><?php echo TOOL_NAME; ?> v<?php echo DASHBOARD_VERSION; ?></span>
                <span class="footer-separator">|</span>
                <span class="footer-author">By <?php echo AUTHOR; ?></span>
            </div>
            <div class="footer-center">
                <span class="footer-update">Last Updated: <span id="last-update-time">--:--:--</span></span>
            </div>
            <div class="footer-right">
                <label class="toggle-label">
                    <input type="checkbox" id="auto-refresh-toggle" checked>
                    <span class="toggle-text">🔄 Auto-refresh</span>
                </label>
                <label class="toggle-label">
                    <input type="checkbox" id="sound-toggle" checked>
                    <span class="toggle-text">🔊 Sound</span>
                </label>
                <button onclick="exportData()" class="btn-export">📥 Export</button>
            </div>
        </footer>
    </div><!-- End Main Container -->
    
    <!-- Notification Sound -->
    <audio id="notification-sound" preload="auto" volume="0.3">
        <source src="data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACAf39/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/gH9/f4B/f3+Af39/g==" type="audio/wav">
    </audio>
    
    <!-- JavaScript -->
    <script>
        <?php include 'assets/js/dashboard.js'; ?>
    </script>
</body>
</html>