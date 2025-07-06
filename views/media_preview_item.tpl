<div class="media-preview-item" data-media-id="{{item.id}}">
    % if item.mime_type.startswith('image'):
    <img src="/media/{{item.wiki_id}}/{{item.uuid_filename}}" alt="{{item.alt_text or item.original_filename}}">
    % else:
    <div class="file-preview">
        <i class="fas fa-file fa-2x"></i>
        <span class="filename">{{item.original_filename}}</span>
    </div>
    % end
    <input type="hidden" name="attached_media[]" value="{{item.id}}">
    <div class="media-actions">
        <button type="button" class="btn btn-sm btn-danger remove-media"
                hx-delete="/media/delete/{{item.id}}"
                hx-target="closest .media-preview-item"
                hx-swap="delete">
            <i class="fas fa-trash"></i>
        </button>
        <button type="button" class="btn btn-sm btn-info edit-media"
                hx-get="/media/edit/{{item.id}}"
                hx-target="next .media-details"
                hx-swap="innerHTML">
            <i class="fas fa-edit"></i>
        </button>
    </div>
    <div class="media-details"></div>
</div>
