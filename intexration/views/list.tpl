<!doctype html>

<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="description" content="InTeXration">
	<meta name="author" content="InTeXration">

	<title>InTeXration</title>

    <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{base_url}}css/style.css">
</head>

<body>
    %include navigation base_url={base_url}

	<div class="container">
		<div class="row">
			<div class="col-md-9">
				% for identifier in documents:
				<div class="document">
					<div class="panel panel-default">
						<div class="panel-heading">{{identifier.name}}</div>
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
					<div class="panel-heading">Statistics</div>
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
					<div class="panel-heading">Configuration</div>
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

	<div id="footer">
    	<div class="container">
     		<p class="credit">InTeXration - LaTeX Continuous Integration Server</p>
    	</div>
    </div>
	<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
	<script src="//code.jquery.com/jquery.js"></script>
	<!-- Include all compiled plugins (below), or include individual files as needed -->
	<script src="//netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
</body>
</html>