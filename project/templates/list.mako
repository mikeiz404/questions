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

% if questions:
    <h1>${len(questions)}
    % if len(questions) == 1:
        Question
    % else:
        Questions
    % endif
    Asked</h1>
    <ul id="questions" class="medium-block-grid-3">
        % for question in questions:
            <li>
                <div class="question panel radius">
                    <span class="content">${question['content']}</span>
                    <span class="actions">
                        <a class="action_remove" href="${request.route_url('remove', id=question['id'])}">[Remove]</a>
                    </span>
                </div>
            </li>
        % endfor
    </ul>
% else:
    <h1>No Questions Asked</h1>
% endif