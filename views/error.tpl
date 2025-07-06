<!DOCTYPE html>
<html>
<head>
    <title>Error {{status_code}}</title>
    <meta charset="utf-8">
    <link rel="stylesheet" href="/static/css/style.css">
    <style>
        :root {
            --error-red: #dc3545;
            --warning-yellow: #ffc107;
            --info-blue: #17a2b8;
            --light-gray: #f8f9fa;
            --border-color: #dee2e6;
        }
        
        body {
            background-color: #f5f7fa;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
        }
        
        .error-container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 30px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.08);
        }
        
        .error-header {
            color: var(--error-red);
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid var(--border-color);
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .error-icon {
            font-size: 2.5rem;
        }
        
        .error-message {
            font-size: 1.25rem;
            margin-bottom: 30px;
            padding: 20px;
            background: #fff5f5;
            border-left: 4px solid var(--error-red);
            border-radius: 4px;
        }
        
        .error-context {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 25px;
            border-left: 4px solid var(--info-blue);
        }
        
        .error-actions {
            margin-top: 30px;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        
        .btn {
            display: inline-flex;
            align-items: center;
            padding: 12px 25px;
            background: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            transition: all 0.2s ease;
            font-weight: 500;
            gap: 8px;
        }
        
        .btn:hover {
            background: #0069d9;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .btn-secondary {
            background: #6c757d;
        }
        
        .btn-secondary:hover {
            background: #5a6268;
        }
        
        .debug-toggle {
            cursor: pointer;
            padding: 12px 20px;
            background: #6c757d;
            color: white;
            border-radius: 6px;
            margin: 25px 0 15px;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-weight: 500;
        }
        
        .debug-toggle:hover {
            background: #5a6268;
        }
        
        .debug-details {
            margin-top: 20px;
            padding: 0;
            background: var(--light-gray);
            border-radius: 8px;
            display: none;
            overflow: hidden;
        }
        
        .debug-section {
            padding: 20px;
            border-bottom: 1px solid var(--border-color);
        }
        
        .debug-section:last-child {
            border-bottom: none;
        }
        
        .debug-section-title {
            font-size: 1.1rem;
            margin-bottom: 15px;
            color: #495057;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .debug-table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 6px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        .debug-table th, .debug-table td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }
        
        .debug-table th {
            background-color: #e9ecef;
            width: 25%;
            font-weight: 600;
        }
        
        .debug-table tr:last-child td {
            border-bottom: none;
        }
        
        .debug-table tr:hover td {
            background-color: #f8f9fa;
        }
        
        .safe-value {
            font-family: monospace;
            word-break: break-all;
            max-width: 800px;
        }
        
        .traceback {
            font-family: monospace;
            white-space: pre-wrap;
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 6px;
            overflow-x: auto;
            font-size: 0.9rem;
            line-height: 1.5;
        }
        
        .timestamp {
            color: #6c757d;
            font-size: 0.9rem;
            margin-top: 10px;
        }
        
        .context-block {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        
        .context-item {
            flex: 1;
            min-width: 300px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        
        .context-item h3 {
            margin-top: 0;
            color: #495057;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 10px;
        }
        
        @media (max-width: 768px) {
            .error-container {
                padding: 20px;
                margin: 15px;
            }
            
            .context-block {
                flex-direction: column;
            }
            
            .btn {
                width: 100%;
                justify-content: center;
            }
        }
    </style>
    <script>
        function toggleDebug() {
            const debugDetails = document.getElementById('debug-details');
            const toggleBtn = document.getElementById('debug-toggle');
            if (debugDetails.style.display === 'none') {
                debugDetails.style.display = 'block';
                toggleBtn.innerHTML = '<i class="fas fa-eye-slash"></i> Hide Debug Details';
            } else {
                debugDetails.style.display = 'none';
                toggleBtn.innerHTML = '<i class="fas fa-bug"></i> Show Debug Details';
            }
        }
        
        function copyDebugInfo() {
            const debugContent = document.getElementById('debug-details').innerText;
            navigator.clipboard.writeText(debugContent).then(() => {
                const copyBtn = document.getElementById('copy-debug');
                copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                setTimeout(() => {
                    copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy Debug Info';
                }, 2000);
            });
        }
    </script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="error-container">
        <div class="error-header">
            <i class="fas fa-exclamation-triangle error-icon"></i>
            <div>
                <h1>Error {{status_code}}</h1>
                </div>
            </div>
        </div>
        
        <div class="error-message">
            <p><strong>Message:</strong> {{error_message}}</p>
            
            % if status_code == 403:
            <p><i class="fas fa-lock"></i> You don't have permission to access this resource.</p>
            % elif status_code == 404:
            <p><i class="fas fa-search"></i> The requested resource could not be found.</p>
            % else:
            <p><i class="fas fa-bug"></i> An unexpected error occurred. Please try again later.</p>
            % end
        </div>
        
        <div class="error-context">
            <h3><i class="fas fa-info-circle"></i> Error Context</h3>
            <div class="context-block">
                <div class="context-item">
                    <h3><i class="fas fa-route"></i> Request</h3>
                    <p><strong>Endpoint:</strong> {{request.path or 'N/A'}}</p>
                    <p><strong>Method:</strong> {{request.method or 'N/A'}}</p>
                    <p><strong>URL:</strong> {{request.url or 'N/A'}}</p>
                </div>
                
                <div class="context-item">
                    <h3><i class="fas fa-user"></i> User</h3>
                    % if user:
                        <p><strong>Username:</strong> {{user.username or 'N/A'}}</p>
                        <p><strong>ID:</strong> {{user.id or 'N/A'}}</p>
                        <p><strong>Role:</strong> {{user.global_role or 'N/A'}}</p>
                    % else:
                        <p>Not authenticated</p>
                    % end
                </div>
            </div>
        </div>
        
        <div class="error-actions">
            <a href="/" class="btn">
                <i class="fas fa-home"></i> Return to Homepage
            </a>
            <a href="javascript:history.back()" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Go Back
            </a>
        </div>
        
        % import os 
        if 'DEBUG' in os.environ and os.environ['DEBUG'] == 'True':
        <div>
            <div id="debug-toggle" class="debug-toggle" onclick="toggleDebug()">
                <i class="fas fa-bug"></i> Show Debug Details
            </div>
            
            <div id="debug-details" class="debug-details">
                <button id="copy-debug" class="btn btn-secondary" onclick="copyDebugInfo()" 
                    style="margin: 15px; padding: 8px 15px; font-size: 0.9rem;">
                    <i class="fas fa-copy"></i> Copy Debug Info
                </button>
                
                <div class="debug-section">
                    <div class="debug-section-title">
                        <i class="fas fa-info-circle"></i>
                        <span>Basic Information</span>
                    </div>
                    <table class="debug-table">
                        <tr>
                            <th>Status Code</th>
                            <td class="safe-value">{{status_code or 'N/A'}}</td>
                        </tr>
                        <tr>
                            <th>Error Message</th>
                            <td class="safe-value">{{error_message or 'N/A'}}</td>
                        </tr>
                        <tr>
                        </tr>
                    </table>
                </div>
                
                <div class="debug-section">
                    <div class="debug-section-title">
                        <i class="fas fa-globe"></i>
                        <span>Request Information</span>
                    </div>
                    <table class="debug-table">
                        <tr>
                            <th>Endpoint</th>
                            <td class="safe-value">{{request.path or 'N/A'}}</td>
                        </tr>
                        <tr>
                            <th>Method</th>
                            <td class="safe-value">{{request.method or 'N/A'}}</td>
                        </tr>
                        <tr>
                            <th>Full URL</th>
                            <td class="safe-value">{{request.url or 'N/A'}}</td>
                        </tr>
                        <tr>
                            <th>Query Parameters</th>
                            <td class="safe-value">
                                % try:
                                    {{dict(request.query)}}
                                % except:
                                    Unable to retrieve query parameters
                                % end
                            </td>
                        </tr>
                        <tr>
                            <th>Form Data</th>
                            <td class="safe-value">
                                % try:
                                    % if request.method == 'POST':
                                        {{dict(request.forms)}}
                                    % else:
                                        N/A (Not a POST request)
                                    % end
                                % except:
                                    Unable to retrieve form data
                                % end
                            </td>
                        </tr>
                    </table>
                </div>
                
                <div class="debug-section">
                    <div class="debug-section-title">
                        <i class="fas fa-user-circle"></i>
                        <span>User Information</span>
                    </div>
                    <table class="debug-table">
                        <tr>
                            <th>Authenticated</th>
                            <td class="safe-value">
                                % if user:
                                    Yes
                                % else:
                                    No
                                % end
                            </td>
                        </tr>
                        % if user:
                        <tr>
                            <th>User ID</th>
                            <td class="safe-value">{{user.id or 'N/A'}}</td>
                        </tr>
                        <tr>
                            <th>Username</th>
                            <td class="safe-value">{{user.username or 'N/A'}}</td>
                        </tr>
                        <tr>
                            <th>Email</th>
                            <td class="safe-value">
                                % try:
                                    {{user.email or 'N/A'}}
                                % except:
                                    Attribute not available
                                % end
                            </td>
                        </tr>
                        <tr>
                            <th>Global Role</th>
                            <td class="safe-value">{{user.global_role or 'N/A'}}</td>
                        </tr>
                        <tr>
                            <th>Wiki Roles</th>
                            <td class="safe-value">
                                % try:
                                    {{user.wiki_roles or '{}'}}
                                % except:
                                    Attribute not available
                                % end
                            </td>
                        </tr>
                        % else:
                        <tr>
                            <td colspan="2">No user information available</td>
                        </tr>
                        % end
                    </table>
                </div>
                
                <div class="debug-section">
                    <div class="debug-section-title">
                        <i class="fas fa-code"></i>
                        <span>Traceback</span>
                    </div>
                    <div class="traceback">
                        % try:
                            {{traceback.format_exc()}}
                        % except:
                            No traceback available
                        % end
                    </div>
                </div>
                
                <div class="debug-section">
                    <div class="debug-section-title">
                        <i class="fas fa-server"></i>
                        <span>Environment Information</span>
                    </div>
                    <table class="debug-table">
                        <tr>
                            <th>Python Version</th>
                            <td class="safe-value">
                                % try:
                                    {{sys.version}}
                                % except:
                                    N/A
                                % end
                            </td>
                        </tr>
                        <tr>
                            <th>Platform</th>
                            <td class="safe-value">
                                % try:
                                    {{sys.platform}}
                                % except:
                                    N/A
                                % end
                            </td>
                        </tr>
                        <tr>
                            <th>Application Path</th>
                            <td class="safe-value">
                                % try:
                                    {{os.getcwd()}}
                                % except:
                                    N/A
                                % end
                            </td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>
        % end
    </div>
</body>
</html>
