$(document).ready(function() {
    /*
        nav highlight when a.href == location.pathname
    */
    $(".nav-sidebar").find("li").each(function() {
        var a = $(this).find("a:first")[0];
        // console.log(a);
        if ($(a).attr("href") === location.pathname) {
            $(this).addClass("active");
        } else {
            $(this).removeClass("active");
        }
    });
});

$(document).ready(function() {
    /*
        nav highlight when a.href == location.pathname
    */
    $(".navbar-nav").find("li").each(function() {
        var a = $(this).find("a:first")[0];
        // console.log(a);
        if ($(a).attr("href") === location.pathname) {
            $(this).addClass("active");
        } else {
            $(this).removeClass("active");
        }
    });
});

$(document).on('shown.bs.modal', '#updateStudent', function(event) {
    var button = $(event.relatedTarget);
    var studentNo = button.data('student-no');
    var modal = $(this);
    var params = {
        "studentNo": studentNo
    };
    $.ajax({
        url: '/admin/getStudent',
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
})

$(document).on('show.bs.modal', '#deleteStudent', function(event) {
    var button = $(event.relatedTarget)
    var studentNo = button.data('student-no')
    var modal = $(this)
    modal.find('#delete-student-no').val(studentNo)
});