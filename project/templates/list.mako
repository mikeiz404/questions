# -*- coding: utf-8 -*-
<%inherit file="layout.mako"/>

<h1>Ask</h1>
<form action="${request.route_url('ask')}" method="POST">
    <div class="row collapse">
        <div class="small-11 columns">
            <input type="text" name="content" placeholder="Question"></input>
        </div>
        <div class="small-1 columns">
            <input type="submit" value="Ask!" name="submit" class="button postfix"></input>
        </div>
    </div>
</form>

<h1>Search</h1>
<form action="${request.route_url('list')}" method="POST">
    <div class="row collapse">
        <div class="small-11 columns">
            <input type="text" name="keywords" placeholder="Question Key Words" value="${keywords}"></input>
        </div>
        <div class="small-1 columns">
            <input type="submit" value="Search!" name="submit" class="button postfix"></input>
        </div>
    </div>
</form>

% if questions:
    <h1>${len(questions)}
    % if len(questions) == 1:
        Question
    % else:
        Questions
    % endif
    % if action == 'search':
        Found
    % else:
        Asked
    %endif
    </h1>
    <ul id="questions" class="medium-block-grid-3">
        % for question in questions:
            <li>
                <div class="question panel radius">
                    <span class="content">${question['content']}</span>
                    <div class="actions">
                        <a class="action_remove" href="${request.route_url('remove', id=question._id)}">[Remove]</a>
                    </div>
                </div>
            </li>
        % endfor
    </ul>
% else:
    <h1>No Questions
    % if action == 'search':
        Found
    % else:
        Asked
    %endif
    </h1>
% endif

% if action == 'search':
    <a class="button" href="${request.route_url('list')}">List All Questions</a>
%endif