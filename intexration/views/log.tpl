%include header base_url=base_url, title=identifier
%include navigation base_url=base_url, doc_link=''

<div class="container">
    % if len(errors) > 0:
    <div class="callout callout-error">
        <h1>Errors</h1>
        <div class="log">
            % for line in errors:
            {{line}} <br/>
            % end
        </div>
    </div>
    % end
    % if len(warnings) > 0:
    <div class="callout callout-warning">
        <h1>Warnings</h1>
        <div class="log">
            % for line in warnings:
            {{line}} <br/>
            % end
        </div>
    </div>
    % end
    <div id="all" class="callout callout-info">
        <h1>Log</h1>
        <div class="log">
            % for line in all:
            {{line}} <br/>
            % end
        </div>
    </div>
</div>

%include footer
