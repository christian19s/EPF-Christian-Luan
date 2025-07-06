% rebase('layout', title='Edit Profile')

<link rel="stylesheet" href="/static/css/edit_user.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<div class="edit-profile-container">
    <h1><i class="fas fa-user-edit"></i> Edit Profile</h1>
    
    % if error:
        <div class="alert alert-error">
            <i class="fas fa-exclamation-circle"></i> {{error}}
        </div>
    % end
    
    % if success:
        <div class="alert alert-success">
            <i class="fas fa-check-circle"></i> {{success}}
        </div>
    % end

    <form method="POST" enctype="multipart/form-data">
        <div class="profile-picture-section">
            <div class="profile-picture-container">
                <img src="{{ user.get_profile_picture_url() }}" 
                     alt="Profile Picture" 
                     class="profile-picture"
                     id="profileImage">
                <input type="file" 
                       name="profile_picture" 
                       id="profileUpload" 
                       accept="image/*" 
                       style="display: none;"
                       onchange="document.getElementById('pictureForm').submit()">
                <button type="button" 
                        class="change-picture-btn"
                        onclick="document.getElementById('profileUpload').click()">
                    <i class="fas fa-camera"></i>
                </button>
            </div>
        </div>

        <div class="form-group">
            <label for="username"><i class="fas fa-user"></i> Username</label>
            <input type="text" id="username" name="username" value="{{ user.username }}" required>
        </div>

        <div class="form-group">
            <label for="email"><i class="fas fa-envelope"></i> Email</label>
            <input type="email" id="email" name="email" value="{{ user.email }}" required>
        </div>

        <div class="form-group">
            <label for="birthdate"><i class="fas fa-birthday-cake"></i> Birthdate</label>
            <input type="date" id="birthdate" name="birthdate" value="{{ user.birthdate or '' }}">
        </div>

        <div class="password-section">
            <h3><i class="fas fa-lock"></i> Change Password</h3>
            
            <div class="form-group password-toggle">
                <label for="current_password">Current Password</label>
                <div class="input-wrapper">
                    <input type="password" id="current_password" name="current_password">
                    <button type="button" class="toggle-btn" onclick="togglePassword('current_password')">
                        <i class="fas fa-eye"></i>
                    </button>
                </div>
            </div>

            <div class="form-group password-toggle">
                <label for="new_password">New Password</label>
                <div class="input-wrapper">
                    <input type="password" id="new_password" name="new_password">
                    <button type="button" class="toggle-btn" onclick="togglePassword('new_password')">
                        <i class="fas fa-eye"></i>
                    </button>
                </div>
            </div>

            <div class="form-group password-toggle">
                <label for="confirm_password">Confirm New Password</label>
                <div class="input-wrapper">
                    <input type="password" id="confirm_password" name="confirm_password">
                    <button type="button" class="toggle-btn" onclick="togglePassword('confirm_password')">
                        <i class="fas fa-eye"></i>
                    </button>
                </div>
            </div>
        </div>

        <button type="submit" class="save-btn">
            <i class="fas fa-save"></i> Save Changes
        </button>
    </form>
</div>

<form id="pictureForm" 
      method="POST" 
      action="/dashboard/update_profile_picture" 
      enctype="multipart/form-data"
      style="display: none;">
</form>

<script>
    function togglePassword(id) {
        const input = document.getElementById(id);
        const icon = input.nextElementSibling.querySelector('i');
        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.replace('fa-eye', 'fa-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.replace('fa-eye-slash', 'fa-eye');
        }
    }
</script>