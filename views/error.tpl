<!DOCTYPE html>
<html>
<head>
    <title>Error {{status_code}}</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
        }
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
    </style>
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
        if 'DEBUG' in os.environ and os.environ['DEBUG'] == 'True':
        <div class="error-details" style="margin-top: 30px; padding: 15px; background: #f8f8f8; border-radius: 4px;">
            <strong>Debug Information:</strong>
            <p>Endpoint: {{request.path}}</p>
            <p>Method: {{request.method}}</p>
            </div>
        % end
    </div>
</body>
</html>
