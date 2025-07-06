<!DOCTYPE html>
<html>
<head>
    <title>Error {{status_code}}</title>
    <meta charset="utf-8">
    <!-- Link to your custom CSS -->
    <link rel="stylesheet" href="/static/css/style.css">
    <style>
        /* Add any additional inline styles here if needed */
        .error-container {
            max-width: 800px;
            margin: 50px auto;
            padding: 30px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .error-header {
            color: #dc3545;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #e9ecef;
        }
        .error-message {
            font-size: 1.2em;
            margin-bottom: 25px;
        }
        .error-actions {
            margin-top: 25px;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            margin-right: 10px;
        }
        .btn:hover {
            background: #0069d9;
        }
        .debug-toggle {
            cursor: pointer;
            padding: 8px 12px;
            background: #6c757d;
            color: white;
            border-radius: 4px;
            margin-bottom: 10px;
            display: inline-block;
        }
        .debug-details {
            margin-top: 30px;
            padding: 15px;
            background: #f8f8f8;
            border-radius: 4px;
            display: none;
        }
        .debug-details table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        .debug-details th, .debug-details td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        .debug-details th {
            background-color: #e9ecef;
            width: 30%;
        }
    </style>
    <script>
        function toggleDebug() {
            const debugDetails = document.getElementById('debug-details');
            const toggleBtn = document.getElementById('debug-toggle');
            if (debugDetails.style.display === 'none') {
                debugDetails.style.display = 'block';
                toggleBtn.textContent = 'Hide Debug Details';
            } else {
                debugDetails.style.display = 'none';
                toggleBtn.textContent = 'Show Debug Details';
            }
        }
    </script>
</head>
<body>
    <div class="error-container">
        <h1 class="error-header">Error {{status_code}}</h1>
        
        <div class="error-message">
            <p>{{error_message}}</p>
            
            % if status_code == 403:
            <p>You don't have permission to access this resource.</p>
            % elif status_code == 404:
            <p>The requested resource could not be found.</p>
            % else:
            <p>An unexpected error occurred. Please try again later.</p>
            % end
        </div>
        
        <div class="error-actions">
            <a href="/" class="btn">Return to Homepage</a>
            <a href="javascript:history.back()" class="btn">Go Back</a>
        </div>
        
        %
        import os 
        import traceback
        from datetime import datetime
        
        if 'DEBUG' in os.environ and os.environ['DEBUG'] == 'True':
        <div style="margin-top: 30px;">
            <div id="debug-toggle" class="debug-toggle" onclick="toggleDebug()">
                Show Debug Details
            </div>
            
            <div id="debug-details" class="debug-details">
                <h3>Debug Information:</h3>
                
                <table>
                    <tr>
                        <th>Endpoint:</th>
                        <td>{{request.path}}</td>
                    </tr>
                    <tr>
                        <th>Method:</th>
                        <td>{{request.method}}</td>
                    </tr>
                    <tr>
                        <th>Full URL:</th>
                        <td>{{request.url}}</td>
                    </tr>
                    <tr>
                        <th>Query Parameters:</th>
                        <td>{{dict(request.query)}}</td>
                    </tr>
                    <tr>
                        <th>Form Data:</th>
                        <td>{{dict(request.forms) if request.method == 'POST' else 'N/A'}}</td>
                    </tr>
                    <tr>
                        <th>User:</th>
                        <td>
                            % if user:
                                {{user.username}} (ID: {{user.id}})
                            % else:
                                Not authenticated
                            % end
                        </td>
                    </tr>
                    <tr>
                        <th>User Permissions:</th>
                        <td>
                            % if user:
                                Global: {{user.global_role}}<br>
                                Wiki Roles: {{user.wiki_roles}}
                            % else:
                                N/A
                            % end
                        </td>
                    </tr>
                </table>
                
                <h4 style="margin-top: 20px;">Request Headers:</h4>
                <table>
                    % for header, value in request.headers.items():
                    <tr>
                        <th>{{header}}</th>
                        <td>{{value}}</td>
                    </tr>
                    % end
                </table>
            </div>
        </div>
        % end
    </div>
</body>
</html>
