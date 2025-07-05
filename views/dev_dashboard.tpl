<!DOCTYPE html>
<html>
<head>
    <title>Dev Dashboard</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, sans-serif; 
            line-height: 1.6; 
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f8f9fa;
        }
        header { 
            background: #2c3e50; 
            color: white; 
            padding: 20px; 
            margin-bottom: 30px;
            border-radius: 5px;
        }
        h1 { margin-bottom: 10px; }
        h2 { 
            color: #2c3e50; 
            padding-bottom: 10px;
            margin: 25px 0 15px;
            border-bottom: 2px solid #eee;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-radius: 5px;
            overflow: hidden;
            margin-bottom: 30px;
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        th {
            background: #3498db;
            color: white;
            font-weight: 600;
        }
        tr:nth-child(even) { background: #f5f7fa; }
        tr:hover { background: #e3f2fd; }
        .count { 
            font-weight: bold; 
            color: #e74c3c;
        }
        .admin-list {
            list-style: none;
            padding: 0;
        }
        .admin-list li {
            padding: 3px 0;
        }
    </style>
</head>
<body>
    <header>
        <h1>Development Dashboard</h1>
        <p>System overview for development purposes</p>
    </header>
    
    <section>
        <h2>All Wikis</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Slug</th>
                    <th>Owner</th>
                    <th>Pages</th>
                    <th>Admins</th>
                </tr>
            </thead>
            <tbody>
                % for wiki in wikis:
                <tr>
                    <td>{{wiki['id']}}</td>
                    <td>{{wiki['name']}}</td>
                    <td>{{wiki['slug']}}</td>
                    <td>{{wiki['owner']}}</td>
                    <td class="count">{{wiki['page_count']}}</td>
                    <td>
                        <ul class="admin-list">
                        % for admin in wiki['admins']:
                            <li>{{admin['username']}} (ID: {{admin['id']}})</li>
                        % end
                        </ul>
                    </td>
                </tr>
                % end
            </tbody>
        </table>
    </section>
    
    <section>
        <h2>All Users</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Role</th>
                </tr>
            </thead>
            <tbody>
                % for user in users:
                <tr>
                    <td>{{user.id}}</td>
                    <td>{{user.username}}</td>
                    <td>{{user.email}}</td>
                    <td>{{user.global_role}}</td>
                </tr>
                % end
            </tbody>
        </table>
    </section>
</body>
</html>
