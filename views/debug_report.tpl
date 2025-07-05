<!DOCTYPE html>
<html>
<head>
    <title>Wiki System Debug Report</title>
    <style>
        :root {
            --success: #4CAF50;
            --error: #F44336;
            --warning: #FFC107;
            --info: #2196F3;
            --neutral: #9E9E9E;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }
        
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
        }
        
        .test-card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            border-left: 5px solid;
            transition: transform 0.2s;
        }
        
        .test-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .success { border-color: var(--success); }
        .error { border-color: var(--error); }
        .warning { border-color: var(--warning); }
        .info { border-color: var(--info); }
        .neutral { border-color: var(--neutral); }
        
        .test-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .test-name {
            font-weight: bold;
            font-size: 1.2em;
        }
        
        .status-badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 0.5px;
        }
        
        .success-badge { background-color: var(--success); }
        .error-badge { background-color: var(--error); }
        .warning-badge { background-color: var(--warning); }
        .info-badge { background-color: var(--info); }
        .neutral-badge { background-color: var(--neutral); }
        
        .test-details {
            background-color: #f8f9fa;
            border-radius: 6px;
            padding: 15px;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 0.95em;
        }
        
        .detail-item {
            margin-bottom: 10px;
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
        }
        
        .detail-item:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }
        
        .detail-key {
            font-weight: bold;
            color: #2c3e50;
            display: inline-block;
            min-width: 180px;
        }
        
        .detail-value {
            color: #555;
            word-break: break-all;
        }
        
        pre {
            background-color: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            margin-top: 10px;
            font-size: 0.9em;
        }
        
        .section-title {
            font-weight: bold;
            color: var(--info);
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <h1>Wiki System Debug Report</h1>
    
    % for test in tests:
        <div class="test-card {{ test['status'] }}">
            <div class="test-header">
                <div class="test-name">{{ test['name'] }}</div>
                <div class="status-badge {{ test['status'] }}-badge">
                    {{ test['status'].upper() }}
                </div>
            </div>
            
            <div class="test-details">
                % for key, value in test['details'].items():
                    % if isinstance(value, dict):
                        <div class="section-title">{{ key.replace('_', ' ').title() }}</div>
                        % for subkey, subvalue in value.items():
                            <div class="detail-item">
                                <span class="detail-key">{{ subkey.replace('_', ' ').title() }}:</span>
                                <span class="detail-value">{{ subvalue }}</span>
                            </div>
                        % end
                    % elif key == 'traceback':
                        <div class="detail-item">
                            <span class="detail-key">Traceback:</span>
                            <pre>{{ value }}</pre>
                        </div>
                    % else:
                        <div class="detail-item">
                            <span class="detail-key">{{ key.replace('_', ' ').title() }}:</span>
                            <span class="detail-value">{{ value }}</span>
                        </div>
                    % end
                % end
            </div>
        </div>
    % end
</body>
</html>
