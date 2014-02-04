%include header base_url=base_url, title='InTeXration'
%include navigation base_url=base_url, doc_link='active'

<div class="container">
    <div class="row">
        <div class="col-md-9">
            % for identifier in documents:
            <div class="document">
                <div class="panel panel-default">
                    <div class="panel-heading"><span class="glyphicon glyphicon-file"></span> <b>{{identifier.name}}</b></div>
                    <table class="table">
                    <tr>
                        <th>Owner</th>
                        <td>{{identifier.owner}}</td>
                        <th>Errors</th>
                        <td>{{len(documents[identifier].errors())}}</td>
                        <th>PDF</th>
                        <td><a href="{{base_url}}pdf/{{identifier.owner}}/{{identifier.repository}}/{{identifier.name}}">link</a></td>
                    </tr>
                    <tr>
                        <th>Repository</th>
                        <td>{{identifier.repository}}</td>
                        <th>Warnings</th>
                        <td>{{len(documents[identifier].warnings())}}</td>
                        <th>Log</th>
                        <td><a href="{{base_url}}log/{{identifier.owner}}/{{identifier.repository}}/{{identifier.name}}">link</a></td>
                    </tr>
                    </table>
                 </div>
            </div>
            % end
        </div>
        <div class="col-md-3">

            <div class="panel panel-default">
                <div class="panel-heading"><span class="glyphicon glyphicon-stats"></span> <b>Statistics</b></div>
                <table class="table">
                <tr>
                    <th>Documents</th>
                    <td>{{len(documents)}}</td>
                </tr>
                <tr>
                    <th>Queued</th>
                    <td>{{len(queue)}}</td>
                </tr>
                </table>
            </div>

            <div class="panel panel-default">
                <div class="panel-heading"><span class="glyphicon glyphicon-wrench"></span> <b>Configuration</b></div>
                <table class="table">
                <tr>
                    <th>Branch</th>
                    <td>{{branch}}</td>
                </tr>
                <tr>
                    <th>Lazy</th>
                    <td>{{lazy}}</td>
                </tr>
                <tr>
                    <th>Threaded</th>
                    <td>{{threaded}}</td>
                </tr>
                </table>
            </div>

        </div>
    </div>
</div>

%include footer
