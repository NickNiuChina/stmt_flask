// not working currently
$(document).ready(function() {

    /*
       nav highlight when a.href == location.pathname
   */

    $(".nav-item").find("li").each(function() {
        var a = $(this).find("a:first")[0];
        // console.log(a);
        if ($(a).attr("href") === location.pathname) {
            $(a).addClass("active");
            console.log("==========================");
        } else {
            $(a).removeClass("active");
            console.log("nnnnnnnnnnnnnnnnnnnnnnnnnnnnn");
        }
    });

    /*
        nav highlight when a.href == location.pathname
    */
    $(".nav-sidebar").find("li").each(function() {
        var a = $(this).find("a:first")[0];
        if ($(a).attr("href") === location.pathname) {
            $(a).addClass("active");
        } else {
            $(a).removeClass("active");
        }
    });

    /*
        admin-student page functions
    */

    // ajax request test
    // $.ajax({
    //         'url': "admin/list/student",
    //         'type': 'get',
    //         'data': {},
    //         'dataType': 'json',
    //         success: function(data) {
    //             console.log(data[0])
    //         }
    //     })
    // {
    //     age: 20,
    //     create_time: "Wed, 02 Dec 2020 00:00:00 GMT",
    // }

    // table students list tb_students_list
    $("#tb_students_list").DataTable({
        // "dom": 'Bfrtip',
        "dom": '<"row"<"col"B><"col"f>>rt<"row"<"col"i><"col"p>>',
        // "dom": '<"container-fluid"<"row"<"col"B><"col"f>>>rt<"row"<"col"i><"col"p>>', //working but container no need
        // "dom": 'Blfrtip',
        "responsive": true,
        // "lengthChange": true,
        "autoWidth": false,
        // "responsive": true, "lengthChange": true, "autoWidth": true,
        "buttons": [{
                extend: 'excel',
                text: 'Excel',
                exportOptions: {
                    modifier: {
                        page: 'all',
                        selected: null,
                        search: 'none',
                    },
                    columns: [0, 1, 2, 3, 4, 5]
                },
            },
            // { extend: 'excel', text: '<i class="fas fa-file-excel" aria-hidden="true"> Excel </i>' },
            "colvis",
            "pageLength"
        ],
        "lengthMenu": [10, 50, 100, "1000"],
        "processing": true,
        "serverSide": true,
        "destroy": true,
        "paging": true,
        "ordering": true,
        "order": [1, "asc"],
        "ajax": {
            'url': "admin/list/student",
            'type': 'post',
            'data': {},
            'dataType': 'json',
        },
        "columnDefs": [{
                "targets": 0,
                "data": null,
                "orderable": false,
                render: function(data, type, row, meta) {
                    return meta.row + 1;
                }
            },
            {
                "targets": 1,
                "data": null,
                "render": function(data, type, row) {
                    return data["student_no"];
                }
            },
            {
                "targets": 2,
                "data": null,
                "render": function(data, type, row) {
                    return data["student_name"];
                }
            },
            {
                "targets": 3,
                "data": null,
                "render": function(data, type, row) {
                    if (data["gender"] == 1) {
                        gender = "M";
                    } else {
                        gender = "F";
                    }
                    return gender;
                }
            },
            {
                "targets": 4,
                "data": null,
                "render": function(data, type, row) {
                    return data["age"];
                }
            },
            {
                "targets": 5,
                "data": null,
                "render": function(data, type, row) {
                    return data["year"];
                }
            },
            {
                "targets": 6,
                "orderable": false,
                "data": null,
                "render": function(data, type, row) {
                    // console.log(data[5]);
                    if (data["student_no"]) {

                        var html = "<button class='btn btn-default' data-student-no=";
                        html += data["student_no"];
                        html += " data-toggle='modal' data-target='#updateStudent'>Edit</button>"
                        html += "<button class='btn btn-danger' data-student-no=";
                        html += data["student_no"];
                        html += " data-toggle='modal' data-target='#deleteStudent'>Delete</button>"
                        return html;
                    }

                }
            },
        ],
    }).buttons().container().appendTo('#tb_students_list .col-md-6:eq(0)');

    $('#updateStudent').on('shown.bs.modal', function(event) {
        var button = $(event.relatedTarget);
        var studentNo = button.data('student-no');
        var modal = $(this);
        var params = {
            "studentNo": studentNo
        };
        $.ajax({
            url: 'admin/getStudent',
            type: "post",
            data: params,
            success: function(result) {
                student = result[0];
                console.log(result);
                modal.find('#update-student-no').val(student.student_no);
                modal.find('#update-student-name').val(student.student_name);
                modal.find('#update-id-card').val(student.id_card);
                modal.find('#update-gender').val(student.gender);
                modal.find('#update-age').val(student.age);
                modal.find('#update-year').val(student.year);
            }
        })
    });

    $(document).on('show.bs.modal', '#deleteStudent', function(event) {
        var button = $(event.relatedTarget);
        var studentNo = button.data('student-no');
        var modal = $(this);
        modal.find('#delete-student-no').val(studentNo);
    });


    /*
        admin-score page functions
    */
    $('#updateScore').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget)
        var scoreId = button.data('score-id')
        var modal = $(this)
        modal.find('#update-id').val(scoreId)
    });


    $('#deleteScore').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget)
        var scoreId = button.data('score-id')
        var modal = $(this)
        modal.find('#delete-score-id').val(scoreId)
    });

    // table score list tb_scores_list
    $("#tb_scores_list").DataTable({
        "dom": 'Blfrtip',
        "responsive": true,
        "lengthChange": true,
        "autoWidth": false,
        // "responsive": true, "lengthChange": true, "autoWidth": true,
        "buttons": ["excel", "colvis"],
        "lengthMenu": [10, 50, 100, "1000"],
        "processing": true,
        "serverSide": true,
        "destroy": true,
        "paging": true,
        "ordering": true,
        "order": [1, "asc"],
        "ajax": {
            'url': "admin/list/score",
            'type': 'post',
            'data': {},
            'dataType': 'json',
        },
        "columnDefs": [{
                "targets": 0,
                "data": null,
                "orderable": false,
                render: function(data, type, row, meta) {
                    return meta.row + 1;
                }
            },
            {
                "targets": 1,
                "data": null,
                "render": function(data, type, row) {
                    return data["student_no"];
                }
            },
            {
                "targets": 2,
                "data": null,
                "render": function(data, type, row) {
                    return data["student_name"];
                }
            },
            {
                "targets": 3,
                "data": null,
                "render": function(data, type, row) {
                    if (data["gender"] == 1) {
                        gender = "M";
                    } else {
                        gender = "F";
                    }
                    return gender;
                }
            },
            {
                "targets": 4,
                "data": null,
                "render": function(data, type, row) {
                    return data["age"];
                }
            },
            {
                "targets": 5,
                "data": null,
                "render": function(data, type, row) {
                    return data["year"];
                }
            },
            {
                "targets": 6,
                "orderable": false,
                "data": null,
                "render": function(data, type, row) {
                    // console.log(data[5]);
                    if (data["student_no"]) {

                        var html = "<button class='btn btn-default' data-student-no=";
                        html += data["student_no"];
                        html += " data-toggle='modal' data-target='#updateStudent'>Edit</button>"
                        html += "<button class='btn btn-danger' data-student-no=";
                        html += data["student_no"];
                        html += " data-toggle='modal' data-target='#deleteStudent'>Delete</button>"
                        return html;
                    }

                }
            },
        ],
    });

    /*
        admin-teacher page functions
    */

    $('#updateTeacher').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget)
        var teacherNo = button.data('teacher-no')
        var modal = $(this)
        var params = {
            "teacherNo": teacherNo
        }
        $.ajax({
            url: 'admin/getTeacher',
            type: "post",
            data: params,
            success: function(result) {
                student = result[0];
                console.log(result);
                modal.find('#update-teacher-no').val(student.teacher_no)
                modal.find('#update-teacher-name').val(student.teacher_name)
                modal.find('#update-gender').val(student.gender)
            }
        })
    });

    $('#deleteTeacher').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget)
        var teacherNo = button.data('teacher-no')
        var modal = $(this)
        modal.find('#delete-teacher-no').val(teacherNo)
    });

    // table score list tb_teachers_list
    $("#tb_teachers_list").DataTable({
        "dom": '<"row"<"col"B><"col"f>>rt<"row"<"col"i><"col"p>>',
        "responsive": true,
        "lengthChange": true,
        "autoWidth": false,
        // "responsive": true, "lengthChange": true, "autoWidth": true,
        "buttons": [{
                extend: 'excel',
                text: 'Excel',
                exportOptions: {
                    modifier: {
                        page: 'all',
                        selected: null,
                        search: 'none',
                    },
                    columns: [0, 1, 2, 3]
                },
            },
            // { extend: 'excel', text: '<i class="fas fa-file-excel" aria-hidden="true"> Excel </i>' },
            "colvis",
            "pageLength"
        ],
        "lengthMenu": [10, 50, 100, "1000"],
        "processing": true,
        "serverSide": true,
        "destroy": true,
        "paging": true,
        "ordering": true,
        "order": [1, "asc"],
        "ajax": {
            'url': "admin/list/teacher",
            'type': 'post',
            'data': {},
            'dataType': 'json',
        },
        "columnDefs": [{
                "targets": 0,
                "data": null,
                "orderable": false,
                render: function(data, type, row, meta) {
                    return meta.row + 1;
                }
            },
            {
                "targets": 1,
                "data": null,
                "render": function(data, type, row) {
                    return data["teacher_no"];
                }
            },
            {
                "targets": 2,
                "data": null,
                "render": function(data, type, row) {
                    return data["teacher_name"];
                }
            },
            {
                "targets": 3,
                "data": null,
                "render": function(data, type, row) {
                    if (data["gender"] == 1) {
                        gender = "M";
                    } else {
                        gender = "F";
                    }
                    return gender;
                }
            },

            {
                "targets": 4,
                "orderable": false,
                "data": null,
                "render": function(data, type, row) {
                    // console.log(data[5]);
                    if (data["teacher_no"]) {

                        var html = "<button class='btn btn-default' data-teacher-no=";
                        html += data["teacher_no"];
                        html += " data-toggle='modal' data-target='#updateTeacher'>Edit</button>"
                        html += "<button class='btn btn-danger' data-teacher-no=";
                        html += data["teacher_no"];
                        html += " data-toggle='modal' data-target='#deleteTeacher'>Delete</button>"
                        return html;
                    }

                }
            },
        ],
    });

    /*
        user management page functions
    */

    // table user list tb_users_list
    $("#tb_users_list").DataTable({
        "dom": '<"row"<"col"B><"col"f>>rt<"row"<"col"i><"col"p>>',
        "responsive": true,
        "lengthChange": true,
        "autoWidth": false,
        // "responsive": true, "lengthChange": true, "autoWidth": true,
        "buttons": [{
                extend: 'excel',
                text: 'Excel',
                exportOptions: {
                    modifier: {
                        page: 'all',
                        selected: null,
                        search: 'none',
                    },
                    columns: [0, 1, 2, 3]
                },
            },
            // { extend: 'excel', text: '<i class="fas fa-file-excel" aria-hidden="true"> Excel </i>' },
            "colvis",
            "pageLength"
        ],
        "lengthMenu": [10, 50, 100, "1000"],
        "processing": true,
        "serverSide": true,
        "destroy": true,
        "paging": true,
        "ordering": true,
        "order": [1, "asc"],
        "ajax": {
            'url': "admin/list/user",
            'type': 'post',
            'data': {},
            'dataType': 'json',
        },
        "columnDefs": [{
                "targets": 0,
                "data": null,
                "orderable": false,
                render: function(data, type, row, meta) {
                    return meta.row + 1;
                }
            },
            {
                "targets": 1,
                "data": null,
                "render": function(data, type, row) {
                    return data["username"];
                }
            },
            {
                "targets": 2,
                "data": null,
                "render": function(data, type, row) {
                    if (data["user_type"] == '1') {
                        return "admin";
                    } else {
                        return "user";
                    }
                }
            },
            {
                "targets": 3,
                "data": null,
                "render": function(data, type, row) {
                    return data["student_no"];
                }
            },
            {
                "targets": 4,
                "data": null,
                "render": function(data, type, row) {
                    if (data["status"] == '2') {
                        return "Disabled";
                    } else {
                        return "Enabled";
                    }
                }
            },

            {
                "targets": 5,
                "orderable": false,
                "data": null,
                "render": function(data, type, row) {
                    // console.log(data[5]);
                    if (data["status"]) {
                        //     <th>
                        //     <button class="btn btn-default" data-user-id="${user.userId }"
                        //         data-toggle="modal" data-target="#changeStatus">禁用</button>
                        //     <button class="btn btn-danger" data-user-id="${user.userId }"
                        //         data-toggle="modal" data-target="#deleteUser">删除</button>
                        // </th>
                        var status = null;
                        var op = null;
                        if (data["username"] != 'admin') {
                            if (data["status"] == '1') {
                                status = "success";
                                op = "Enabled";
                            } else {
                                status = "danger";
                                op = "Disabled";
                            }
                            var html = "<button class='btn btn-" + status + "' data-username=";
                            html += data["username"];
                            html += " data-user-status=" + data["status"]
                            html += " id='changeStatus'>" + op + "</button>"
                            html += "<button class='btn btn-danger' data-username=";
                            html += data["username"];
                            html += " data-toggle='modal' data-target='#deleteUser'>Delete</button>"
                            return html;
                        } else {
                            return "HIDED!";
                        }
                    }

                }
            },
        ],
    });

    $('#deleteUser').on('shown.bs.modal', function(event) {
        var button = $(event.relatedTarget);
        var username = button.data('username');
        var modal = $(this);
        console.log(username);
        modal.find('#delete-username').val(username);

        // submit in html
        // $(this).on('click', '#delete_student', { 'username': username }, function(e) {
        //     console.log(username);
        //     if (username) {
        //         $.post("admin/delete/user", { 'username': username, 'op': "delete" }, function(result) {
        //             // $('#tb_users_list').DataTable().ajax.reload(); // reload table data
        //             $('#deleteUser').modal('hide'); // hide modal
        //         });
        //     }
        // });
    });

    // $('#clientStatusModal').on('shown.bs.modal',
    //     function(e) {
    //         storename = $(e.relatedTarget).parent().parent().children(".dtr-control").text();
    //         cn = $(e.relatedTarget).parent().parent().children(".dtr-control").next().text();
    //         var thismodal = $('#clientStatusModal');
    //         thismodal.find('.modal-body').html("<p>storename: " + storename + "</p><p>cn: " + cn + "</p>");
    //         $(this).on('click', '.btn-primary', { 'filename': cn }, function(e) {
    //             var newstorename = thismodal.find('input').val();
    //             console.log("newstorename:" + newstorename);
    //             if (newstorename) {
    //                 $.post("service/clientstatus/update", { 'cn': cn, 'newstorename': newstorename }, function(result) {
    //                     $('#tbclientstatus').DataTable().ajax.reload(); // reload table data
    //                     $('#clientStatusModal').modal('hide'); // hide modal
    //                 });
    //             }
    //         });

    //     });

    $(document).on('click', '#changeStatus', function(e) {
        // storename = $(e.relatedTarget).parent().parent().children(".dtr-control").text();
        // var test = $(e.target).text(); // button word
        var target_user = $(e.target).parent().parent().children().eq(1).text();
        var user_status = $(e.target).data('user-status');
        console.log(target_user + ", " + user_status);

        $.post("admin/user/toggle", { 'target_user': target_user, "user_status": user_status }, function(result) {
            // console.log(result)
            $('#tb_users_list').DataTable().ajax.reload();
        });
    });
    // $(document).on('click', '#changeStatus', function() {
    //     alert("button is clicked");
    // });

});